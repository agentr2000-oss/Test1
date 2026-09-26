"""Build the Preclinical Tools Monitor page from the dataset CSVs.

    python dashboard/build_dashboard.py      # run from data/preclinical-tools-spend/

Reads indicators.csv, observations.csv, auto/*.csv and latest.csv, embeds them as JSON in
template.html and writes preclinical-tools-monitor.html next to this script. Run
`python tracker.py latest` first so latest.csv is current.
"""

import csv
import datetime as dt
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
TEMPLATE = os.path.join(HERE, "template.html")
OUT = os.path.join(HERE, "preclinical-tools-monitor.html")


def read_csv(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def to_float(s):
    try:
        return float(s)
    except (TypeError, ValueError):
        return None


def main():
    catalog = read_csv(os.path.join(ROOT, "indicators.csv"))
    paths = [os.path.join(ROOT, "observations.csv")]
    auto = os.path.join(ROOT, "auto")
    if os.path.isdir(auto):
        paths += [os.path.join(auto, n) for n in sorted(os.listdir(auto)) if n.endswith(".csv")]

    obs = {}
    total = 0
    for path in paths:
        for r in read_csv(path):
            obs.setdefault(r["indicator_id"], []).append({
                "p": r["period"], "e": r["period_end"], "v": to_float(r["value"]), "u": r["unit"],
                "t": r["value_text"], "s": r["source_name"], "su": r["source_url"], "no": r["notes"],
            })
            total += 1

    today = dt.date.today().isoformat()
    as_of = max((o["e"] for rows in obs.values() for o in rows if o["e"] <= today), default=today)
    ids = {c["indicator_id"] for c in catalog}
    data = {
        "asOf": as_of,
        "counts": {"obs": total, "catalog": len(catalog), "withData": len(ids & set(obs))},
        "obs": obs,
        "latest": read_csv(os.path.join(ROOT, "latest.csv")),
    }
    payload = json.dumps(data, separators=(",", ":"), ensure_ascii=False).replace("</", "<\\/")
    with open(TEMPLATE) as f:
        page = f.read()
    marker = "/*__DATA__*/null"
    if marker not in page:
        raise SystemExit("template.html is missing the /*__DATA__*/null marker")
    with open(OUT, "w") as f:
        f.write(page.replace(marker, payload))
    print(f"wrote {os.path.relpath(OUT, ROOT)} ({len(page) + len(payload):,} bytes; {total} observations, as of {as_of})")


if __name__ == "__main__":
    main()
