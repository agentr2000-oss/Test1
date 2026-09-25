"""Preclinical tools spend tracker: refresh, validate, and summarize the dataset.

Stdlib only (Python 3.9+). Three subcommands:

    python tracker.py fetch   # pull the free-API ("auto") series into auto/*.csv
    python tracker.py check   # validate observations.csv + auto/*.csv against indicators.csv
    python tracker.py latest  # write latest.csv: newest reading per indicator with prior-period change

`fetch` needs normal internet access. SEC sources also need a contact string in the
SEC_USER_AGENT env var (SEC fair-access policy), e.g.
    SEC_USER_AGENT="Jane Doe jane@example.com" python tracker.py fetch
Pick sources with --sources fred,nih,sec,formd,ctgov and a start month with --start 2021-01.
"""

import argparse
import calendar
import csv
import datetime as dt
import io
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
AUTO_DIR = os.path.join(HERE, "auto")
CACHE_DIR = os.path.join(AUTO_DIR, "cache")
INDICATORS_CSV = os.path.join(HERE, "indicators.csv")
OBSERVATIONS_CSV = os.path.join(HERE, "observations.csv")
LATEST_CSV = os.path.join(HERE, "latest.csv")

OBS_FIELDS = ["indicator_id", "period", "period_end", "value", "unit", "value_text",
              "source_name", "source_url", "notes"]

# --- Series definitions ------------------------------------------------------------

# indicator_id -> (FRED series id, unit)
FRED_SERIES = {
    "MACRO_M3_INSTR_NEW_ORDERS": ("A34KNO", "USD_mn"),
    "MACRO_M3_INSTR_UNFILLED": ("A34KUO", "USD_mn"),
    "MACRO_IP_INSTR": ("IPG3345S", "index_2017=100"),
    "MACRO_PPI_LAB_INSTR": ("PCU334516334516", "index_dec1985=100"),
    "MACRO_PPI_SCI_INSTR": ("WPU1185", "index_dec1982=100"),
    "MACRO_EMP_SCI_RD": ("CES6054170001", "thousands"),
    "MACRO_EMP_PHARMA_MFG": ("CES3232540001", "thousands"),
    "MACRO_INDEED_SCI_RD": ("IHLIDXUSTPSCREDE", "index_feb2020=100"),
    "MACRO_UST10Y": ("GS10", "pct"),
    "MACRO_FEDFUNDS": ("FEDFUNDS", "pct"),
}

# ticker -> SEC CIK. Pharma R&D budgets (demand) and tools/CRO revenue (the outcome to predict).
PHARMA_CIKS = {
    "PFE": 78003, "MRK": 310158, "JNJ": 200406, "LLY": 59478, "ABBV": 1551152,
    "BMY": 14272, "AMGN": 318154, "GILD": 882095, "REGN": 872589, "VRTX": 875320,
}
TOOLS_CIKS = {
    "TMO": 97745, "DHR": 313616, "A": 1090872, "WAT": 1000697, "BRKR": 1109354,
    "RVTY": 31791, "TECH": 842023, "MTD": 1037646, "AVTR": 1722482, "CRL": 1100682,
}
RD_TAGS = ["ResearchAndDevelopmentExpense",
           "ResearchAndDevelopmentExpenseExcludingAcquiredInProcessCost"]
REVENUE_TAGS = ["RevenueFromContractWithCustomerExcludingAssessedTax", "Revenues",
                "SalesRevenueNet"]

FORMD_INDUSTRIES = {"Biotechnology", "Pharmaceuticals"}
US_STATES = set("""AL AK AZ AR CA CO CT DE DC FL GA HI ID IL IN IA KS KY LA ME MD MA MI MN MS
MO MT NE NV NH NJ NM NY NC ND OH OK OR PA RI SC SD TN TX UT VT VA WA WV WI WY""".split())

REPORTER_URL = "https://api.reporter.nih.gov/v2/projects/search"
CTGOV_URL = "https://clinicaltrials.gov/api/v2/studies"


# --- Helpers -------------------------------------------------------------------------

def http(url, headers=None, body=None, timeout=90, retries=4):
    """GET (or POST when body is given) with exponential backoff on transient errors."""
    headers = dict(headers or {})
    data = None
    if body is not None:
        data = json.dumps(body).encode()
        headers.setdefault("Content-Type", "application/json")
    headers.setdefault("User-Agent", "preclinical-tools-spend-tracker/1.0")
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, data=data, headers=headers)
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.read()
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504) and attempt < retries - 1:
                time.sleep(2 ** (attempt + 1))
                continue
            raise
        except urllib.error.URLError:
            if attempt < retries - 1:
                time.sleep(2 ** (attempt + 1))
                continue
            raise


def month_end(year, month):
    return dt.date(year, month, calendar.monthrange(year, month)[1])


def iter_months(start, end):
    """Yield (year, month) from start to end inclusive; both are (year, month) tuples."""
    y, m = start
    while (y, m) <= end:
        yield y, m
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)


def last_complete_month(today=None):
    today = today or dt.date.today()
    first = today.replace(day=1)
    prev = first - dt.timedelta(days=1)
    return prev.year, prev.month


def quarter_label(d):
    return f"{d.year}-Q{(d.month - 1) // 3 + 1}"


def parse_date(s):
    s = (s or "").strip().split("T")[0].split(" ")[0]
    for fmt in ("%Y-%m-%d", "%d-%b-%Y", "%m/%d/%Y"):
        try:
            return dt.datetime.strptime(s, fmt).date()
        except ValueError:
            continue
    return None


def to_float(s):
    try:
        return float(str(s).replace(",", "").strip())
    except (TypeError, ValueError):
        return None


def fmt_num(x, nd=3):
    if x is None:
        return ""
    return f"{x:.{nd}f}".rstrip("0").rstrip(".")


def row(indicator_id, period, period_end, value, unit, source_name, source_url, notes="", value_text=""):
    return {"indicator_id": indicator_id, "period": period, "period_end": str(period_end),
            "value": value if isinstance(value, str) else fmt_num(value), "unit": unit,
            "value_text": value_text, "source_name": source_name, "source_url": source_url,
            "notes": notes}


def write_rows(path, rows):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    rows = sorted(rows, key=lambda r: (r["indicator_id"], r["period_end"]))
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=OBS_FIELDS)
        w.writeheader()
        w.writerows(rows)
    print(f"  wrote {len(rows)} rows -> {os.path.relpath(path, HERE)}")


def read_csv(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def sec_headers():
    ua = os.environ.get("SEC_USER_AGENT", "").strip()
    if not ua:
        return None
    return {"User-Agent": ua, "Accept-Encoding": "identity"}


# --- Fetchers ------------------------------------------------------------------------

def fetch_fred(start):
    """Monthly FRED series via the keyless fredgraph CSV endpoint. Daily/weekly series are
    averaged to months."""
    rows = []
    for ind, (sid, unit) in FRED_SERIES.items():
        url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={sid}&cosd={start[0]}-{start[1]:02d}-01"
        try:
            text = http(url).decode()
        except Exception as e:  # noqa: BLE001 - keep going if one series fails
            print(f"  FRED {sid}: {e}", file=sys.stderr)
            continue
        by_month = defaultdict(list)
        reader = csv.reader(io.StringIO(text))
        next(reader, None)  # header: observation_date (or DATE), <sid>
        for rec in reader:
            if len(rec) < 2:
                continue
            d, v = parse_date(rec[0]), to_float(rec[1])
            if d and v is not None:
                by_month[(d.year, d.month)].append(v)
        for (y, m), vals in sorted(by_month.items()):
            note = f"monthly mean of {len(vals)} obs" if len(vals) > 1 else ""
            rows.append(row(ind, f"{y}-{m:02d}", month_end(y, m), sum(vals) / len(vals), unit,
                            "FRED", f"https://fred.stlouisfed.org/series/{sid}", note))
        print(f"  FRED {sid}: {len(by_month)} months")
    return rows


def reporter_search(criteria, offset=0, limit=500, fields=None):
    body = {"criteria": criteria, "offset": offset, "limit": limit}
    if fields:
        body["include_fields"] = fields
    return json.loads(http(REPORTER_URL, body=body))


def fetch_nih(start, end):
    """New (Type 1) NIH awards and S10 instrumentation awards by Notice of Award month."""
    rows = []
    src = "NIH RePORTER API"
    url = "https://reporter.nih.gov/"
    for y, m in iter_months(start, end):
        window = {"from_date": f"{y}-{m:02d}-01", "to_date": str(month_end(y, m))}
        base = {"award_notice_date": window, "exclude_subprojects": True}
        for ind_prefix, extra in (("ACAD_NIH_NEW_AWARDS", {"award_types": ["1"]}),
                                  ("ACAD_NIH_S10", {"activity_codes": ["S10"]})):
            crit = {**base, **extra}
            total, dollars, offset = None, 0.0, 0
            try:
                while True:
                    res = reporter_search(crit, offset=offset,
                                          fields=["ApplId", "AwardAmount", "AwardNoticeDate"])
                    total = res.get("meta", {}).get("total", 0)
                    results = res.get("results", []) or []
                    dollars += sum(to_float(r.get("award_amount")) or 0 for r in results)
                    offset += len(results)
                    if not results or offset >= total or offset >= 14500:
                        break
                    time.sleep(1)  # RePORTER asks for <= 1 request/second
            except Exception as e:  # noqa: BLE001
                print(f"  RePORTER {ind_prefix} {y}-{m:02d}: {e}", file=sys.stderr)
                continue
            note = "award_notice_date in month; excludes subprojects; RePORTER covers NIH plus a few other HHS agencies"
            if offset < (total or 0):
                note += f"; USD summed over first {offset} of {total} awards"
            pe = month_end(y, m)
            rows.append(row(f"{ind_prefix}_N", f"{y}-{m:02d}", pe, float(total or 0), "count", src, url, note))
            rows.append(row(f"{ind_prefix}_USD", f"{y}-{m:02d}", pe, dollars / 1e6, "USD_mn", src, url, note))
            time.sleep(1)
        print(f"  RePORTER {y}-{m:02d} done")
    return rows


def xbrl_facts(cik, tags, headers):
    """Merge USD duration facts for the first tag that has each (start, end) period."""
    facts = {}
    for tag in tags:
        url = f"https://data.sec.gov/api/xbrl/companyconcept/CIK{cik:010d}/us-gaap/{tag}.json"
        try:
            data = json.loads(http(url, headers=headers))
        except urllib.error.HTTPError as e:
            if e.code == 404:
                continue
            raise
        found = {}
        for f in data.get("units", {}).get("USD", []):
            s, e_ = parse_date(f.get("start")), parse_date(f.get("end"))
            if not s or not e_:
                continue
            key = (s, e_)
            if key not in found or f.get("filed", "") > found[key]["filed"]:
                found[key] = {"val": f["val"], "filed": f.get("filed", ""), "tag": tag}
        for key, v in found.items():
            facts.setdefault(key, v)
        time.sleep(0.2)  # stay well under SEC's 10 req/s
    return facts


def quarterly_from_facts(facts):
    """Return {quarter_end: (value, derived?)} using ~3-month facts, deriving Q4 = FY - Q1..Q3."""
    quarters = {e: v["val"] for (s, e), v in facts.items() if 80 <= (e - s).days <= 100}
    for (s, e), v in facts.items():
        if 350 <= (e - s).days <= 380 and e not in quarters:
            inside = [q for q in quarters if s < q < e]
            if len(inside) == 3:
                quarters[e] = v["val"] - sum(quarters[q] for q in inside)
    return dict(sorted(quarters.items()))


def fetch_sec_xbrl(start):
    headers = sec_headers()
    if not headers:
        print("  SEC XBRL skipped: set SEC_USER_AGENT='Name email@domain'", file=sys.stderr)
        return []
    start_date = dt.date(start[0], start[1], 1)
    rows = []
    groups = (("PHARMA_RD", PHARMA_CIKS, RD_TAGS, "R&D expense"),
              ("TOOLS_REV", TOOLS_CIKS, REVENUE_TAGS, "revenue"))
    for prefix, ciks, tags, label in groups:
        per_company = {}
        for ticker, cik in ciks.items():
            try:
                q = quarterly_from_facts(xbrl_facts(cik, tags, headers))
            except Exception as e:  # noqa: BLE001
                print(f"  SEC {ticker}: {e}", file=sys.stderr)
                continue
            if not q:
                print(f"  SEC {ticker}: no quarterly facts for {tags}", file=sys.stderr)
                continue
            per_company[ticker] = {quarter_label(d - dt.timedelta(days=10)): (d, v) for d, v in q.items()}
            src_url = f"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={cik}&type=10-Q"
            for lbl, (d, v) in per_company[ticker].items():
                if d >= start_date:
                    rows.append(row(f"{prefix}_{ticker}_Q", lbl, d, v / 1e6, "USD_mn", "SEC XBRL (10-Q/10-K)",
                                    src_url, f"GAAP {label}; quarter labelled by fiscal quarter-end date; Q4 derived as FY minus Q1-Q3"))
            print(f"  SEC {ticker}: {len(q)} quarters")
        # Basket y/y growth over quarters where every company reported both years.
        labels = sorted({lbl for comp in per_company.values() for lbl in comp})
        for lbl in labels:
            y, qn = int(lbl[:4]), lbl[5:]
            prior = f"{y - 1}-{qn}"
            if not per_company or not all(lbl in c and prior in c for c in per_company.values()):
                continue
            cur = sum(c[lbl][1] for c in per_company.values())
            prev = sum(c[prior][1] for c in per_company.values())
            d = max(c[lbl][0] for c in per_company.values())
            if d >= start_date and prev:
                basket = "TOP10" if prefix == "PHARMA_RD" else "BASKET"
                rows.append(row(f"{prefix}_{basket}_Q_YOY", lbl, d, (cur / prev - 1) * 100, "pct",
                                "SEC XBRL (derived)", "https://www.sec.gov/edgar/sec-api-documentation",
                                f"reported (not organic) y/y growth of summed {label} for {', '.join(sorted(per_company))}"))
    return rows


def fetch_formd(start, end):
    """New Form D notices from US biotech/pharma issuers, per SEC Form D quarterly data set."""
    headers = sec_headers()
    if not headers:
        print("  Form D skipped: set SEC_USER_AGENT='Name email@domain'", file=sys.stderr)
        return []
    os.makedirs(CACHE_DIR, exist_ok=True)
    rows = []
    quarters = sorted({(y, (m - 1) // 3 + 1) for y, m in iter_months(start, end)})
    for y, qn in quarters:
        name = f"{y}q{qn}_d.zip"
        cache = os.path.join(CACHE_DIR, name)
        if not os.path.exists(cache):
            url = f"https://www.sec.gov/files/structureddata/data/form-d-data-sets/{name}"
            try:
                blob = http(url, headers=headers, timeout=300)
            except urllib.error.HTTPError as e:
                print(f"  Form D {name}: HTTP {e.code} (not published yet?)", file=sys.stderr)
                continue
            with open(cache, "wb") as f:
                f.write(blob)
        tables = {}
        with zipfile.ZipFile(cache) as z:
            for member in z.namelist():
                base = os.path.basename(member).upper()
                if base in ("FORMDSUBMISSION.TSV", "ISSUERS.TSV", "OFFERING.TSV"):
                    text = z.read(member).decode("utf-8", errors="replace")
                    rdr = csv.DictReader(io.StringIO(text), delimiter="\t")
                    tables[base] = [{k.upper(): (v or "") for k, v in r.items() if k} for r in rdr]
        if len(tables) < 3:
            print(f"  Form D {name}: expected tables missing, found {sorted(tables)}", file=sys.stderr)
            continue
        new_filings = {r["ACCESSIONNUMBER"] for r in tables["FORMDSUBMISSION.TSV"]
                       if r.get("SUBMISSIONTYPE", "").strip().upper() == "D"}
        us_issuers = {r["ACCESSIONNUMBER"] for r in tables["ISSUERS.TSV"]
                      if r.get("IS_PRIMARYISSUER_FLAG", "").upper() in ("YES", "Y", "TRUE", "1")
                      and r.get("STATEORCOUNTRY", "").strip().upper() in US_STATES}
        n, usd = 0, 0.0
        for r in tables["OFFERING.TSV"]:
            acc = r["ACCESSIONNUMBER"]
            if acc in new_filings and acc in us_issuers and r.get("INDUSTRYGROUPTYPE", "").strip() in FORMD_INDUSTRIES:
                n += 1
                usd += to_float(r.get("TOTALAMOUNTSOLD")) or 0
        pe = month_end(y, qn * 3)
        src_url = "https://www.sec.gov/data-research/sec-markets-data/form-d-data-sets"
        note = "new Form D notices (excl. amendments), primary issuer in a US state, industry group Biotechnology or Pharmaceuticals"
        rows.append(row("BIO_FORMD_N", f"{y}-Q{qn}", pe, float(n), "count", "SEC Form D data sets", src_url, note))
        rows.append(row("BIO_FORMD_USD", f"{y}-Q{qn}", pe, usd / 1e9, "USD_bn", "SEC Form D data sets", src_url,
                        note + "; sum of totalAmountSold at filing"))
        print(f"  Form D {y}-Q{qn}: {n} filings, ${usd / 1e9:.2f}bn")
    return rows


def fetch_ctgov(start, end):
    """Industry-sponsored Phase 1 / Early Phase 1 study starts with a US site, by start month.
    A confirming (lagging) signal: preclinical programs graduating into the clinic."""
    rows = []
    for y, m in iter_months(start, end):
        expr = (f"AREA[StartDate]RANGE[{y}-{m:02d}-01,{month_end(y, m)}] "
                "AND AREA[Phase](PHASE1 OR EARLY_PHASE1) "
                "AND AREA[LeadSponsorClass]INDUSTRY "
                'AND AREA[LocationCountry]"United States"')
        qs = urllib.parse.urlencode({"filter.advanced": expr, "countTotal": "true",
                                     "pageSize": "1", "fields": "NCTId"})
        try:
            total = json.loads(http(f"{CTGOV_URL}?{qs}")).get("totalCount")
        except Exception as e:  # noqa: BLE001
            print(f"  ClinicalTrials.gov {y}-{m:02d}: {e}", file=sys.stderr)
            continue
        rows.append(row("CONF_CTGOV_PH1_STARTS_US", f"{y}-{m:02d}", month_end(y, m), float(total or 0), "count",
                        "ClinicalTrials.gov API v2", "https://clinicaltrials.gov/data-api/api",
                        "industry lead sponsor, Phase 1 or Early Phase 1, >=1 US site, by (actual or anticipated) start date; recent months revise up"))
        time.sleep(0.5)
    print(f"  ClinicalTrials.gov: {len(rows)} months")
    return rows


# --- Commands ------------------------------------------------------------------------

def cmd_fetch(args):
    start = tuple(int(x) for x in args.start.split("-"))
    end = last_complete_month()
    sources = [s.strip() for s in args.sources.split(",") if s.strip()]
    jobs = {
        "fred": lambda: fetch_fred(start),
        "nih": lambda: fetch_nih(start, end),
        "sec": lambda: fetch_sec_xbrl(start),
        "formd": lambda: fetch_formd(start, end),
        "ctgov": lambda: fetch_ctgov(start, end),
    }
    for s in sources:
        if s not in jobs:
            sys.exit(f"unknown source {s!r}; choose from {', '.join(jobs)}")
        print(f"[{s}]")
        rows = jobs[s]()
        if rows:
            write_rows(os.path.join(AUTO_DIR, f"{s}.csv"), rows)
        else:
            print("  no rows fetched; existing file left untouched")


def load_all_observations():
    paths = [("observations.csv", OBSERVATIONS_CSV)]
    if os.path.isdir(AUTO_DIR):
        paths += [(f"auto/{n}", os.path.join(AUTO_DIR, n)) for n in sorted(os.listdir(AUTO_DIR)) if n.endswith(".csv")]
    rows = []
    for origin, path in paths:
        rows += [dict(r, origin=f"{origin} line {i}") for i, r in enumerate(read_csv(path), start=2)]
    return rows


def catalog():
    return {r["indicator_id"]: r for r in read_csv(INDICATORS_CSV)}


def cmd_check(_args):
    cat = catalog()
    problems = []
    for r in load_all_observations():
        where = f"{r['origin']} ({r.get('indicator_id')})"
        if r["indicator_id"] not in cat:
            problems.append(f"{where}: indicator_id not in indicators.csv")
        if not parse_date(r.get("period_end")):
            problems.append(f"{where}: bad period_end {r.get('period_end')!r}")
        if r.get("value") and to_float(r["value"]) is None:
            problems.append(f"{where}: non-numeric value {r['value']!r}")
        if not r.get("value") and not r.get("value_text"):
            problems.append(f"{where}: needs value or value_text")
        if not (r.get("source_url") or "").startswith("http"):
            problems.append(f"{where}: missing source_url")
    for p in problems:
        print(p)
    print(f"{len(problems)} problem(s)")
    return 1 if problems else 0


def cmd_latest(_args):
    cat = catalog()
    by_ind = defaultdict(list)
    for r in load_all_observations():
        d = parse_date(r.get("period_end"))
        if d and (r.get("value") or r.get("value_text")):
            by_ind[r["indicator_id"]].append((d, r))
    out = []
    for ind, items in by_ind.items():
        items.sort(key=lambda t: t[0])
        d, cur = items[-1]
        prev = next((r for pd, r in reversed(items[:-1])
                     if pd < d and r.get("unit") == cur.get("unit") and to_float(r.get("value")) is not None), None)
        change = ""
        if prev and to_float(cur.get("value")) is not None:
            change = fmt_num(to_float(cur["value"]) - to_float(prev["value"]))
        meta = cat.get(ind, {})
        out.append({
            "channel": meta.get("channel", ""), "indicator_id": ind, "name": meta.get("name", ""),
            "period": cur["period"], "period_end": cur["period_end"], "value": cur.get("value", ""),
            "unit": cur.get("unit", ""), "value_text": cur.get("value_text", ""),
            "prev_period": prev["period"] if prev else "", "prev_value": prev["value"] if prev else "",
            "change_vs_prev": change, "read_as": meta.get("read_as", ""), "source_url": cur.get("source_url", ""),
        })
    out.sort(key=lambda r: (r["channel"], r["indicator_id"]))
    with open(LATEST_CSV, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0].keys()) if out else ["indicator_id"])
        w.writeheader()
        w.writerows(out)
    print(f"wrote {len(out)} indicators -> latest.csv")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    f = sub.add_parser("fetch", help="refresh auto/*.csv from free public APIs")
    f.add_argument("--sources", default="fred,nih,sec,formd,ctgov")
    f.add_argument("--start", default="2021-01", help="first month, YYYY-MM")
    sub.add_parser("check", help="validate observations against the indicator catalog")
    sub.add_parser("latest", help="write latest.csv")
    args = p.parse_args()
    return {"fetch": cmd_fetch, "check": cmd_check, "latest": cmd_latest}[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main() or 0)
