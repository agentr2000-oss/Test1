# US Preclinical Tools Spend: Leading Indicators Dataset

A cited, refreshable dataset of **leading indicators for US preclinical "picks and shovels" spend**: lab instruments, consumables, research models and outsourced preclinical studies. It covers the three buyer groups that fund that spend:

| Buyer group | Money trail | Where it shows up first |
|---|---|---|
| **Academic & government** | Appropriations → NIH/NSF grant awards → lab budgets → instruments and consumables | NIH budget, award pace, S10 instrument grants, IDC policy |
| **Biotech** | VC, IPOs and follow-ons → hiring → lab buildouts → orders | Venture $, IPO window, XBI, layoffs, lab vacancy, Form D |
| **Pharma R&D** | R&D budgets → internal discovery + outsourced preclinical studies | Big-pharma R&D spend, Charles River DSA bookings |

Tools-vendor readouts (end-market growth, orders, guidance) and a few macro series (instrument orders, R&D hiring, rates) sit alongside. Vendor revenue is included as the **outcome** the leading indicators should predict.

_Started 2026-09-25. Idea note: [`ideas/2026-09-25-preclinical-tools-spend-tracker.md`](../../ideas/2026-09-25-preclinical-tools-spend-tracker.md)._

<!-- CURRENT_READ -->

## Files

| File | What it is |
|---|---|
| [`indicators.csv`](indicators.csv) | **Catalog.** One row per indicator: channel, signal role (leading / coincident / confirming / structural / target), typical lead time, how to read it (`higher = bullish` etc.), frequency, unit, series reference, source and access (free/paid). |
| [`observations.csv`](observations.csv) | **Curated data**, researched and cited row by row: budgets, grant stats, VC and IPO totals, CRO bookings, pharma R&D, vendor end-market commentary, policy events. |
| `auto/*.csv` | **API-refreshed data** from `tracker.py fetch`: FRED, NIH RePORTER, SEC XBRL, SEC Form D and ClinicalTrials.gov. Same columns as `observations.csv`. |
| [`latest.csv`](latest.csv) | Newest reading per indicator, with the prior reading and the change. Rebuilt by `tracker.py latest`. |
| [`tracker.py`](tracker.py) | Refresh / validate / summarize script. Python 3.9+, standard library only. |

### Observation schema (long format)

`indicator_id, period, period_end, value, unit, value_text, source_name, source_url, notes`

- `period`: `2026-Q2`, `2026-08`, `2025` (calendar year), `FY2025` (US federal FY, ends Sep 30), or a company fiscal label such as `FY2026-Q3` (explained in `notes`).
- `value` is numeric (no `$`, `%` or `x`). Qualitative readings and events go in `value_text`, for example "declined mid-single digits" or a court ruling.
- Every row has a `source_url`. Numbers were only recorded when a source stated them explicitly; nothing is interpolated.

## Refreshing

```bash
cd data/preclinical-tools-spend
# SEC asks for a contact string in the User-Agent (fair-access policy)
export SEC_USER_AGENT="Your Name you@example.com"
python tracker.py fetch                  # all sources, from 2021-01
python tracker.py fetch --sources fred,nih --start 2019-01
python tracker.py check                  # validate every row against the catalog
python tracker.py latest                 # rebuild latest.csv
```

| Source | What gets pulled | Docs |
|---|---|---|
| FRED (keyless CSV) | Census M3 instrument orders and backlog, instrument industrial production, lab-instrument PPI, R&D and pharma employment, Indeed R&D job postings, rates | https://fred.stlouisfed.org/ |
| NIH RePORTER API | Monthly count and $ of new (Type 1) NIH awards and S10 instrumentation awards, by Notice of Award date | https://api.reporter.nih.gov/ |
| SEC XBRL API | Quarterly GAAP R&D for 10 big US pharmas, and quarterly revenue for 10 tools and CRO companies, plus basket y/y growth | https://www.sec.gov/edgar/sec-api-documentation |
| SEC Form D data sets | Quarterly count and $ of new private raises by US biotech and pharma issuers: a free proxy for paywalled VC databases | https://www.sec.gov/data-research/sec-markets-data/form-d-data-sets |
| ClinicalTrials.gov API v2 | Monthly industry-sponsored Phase 1 starts with a US site (confirms that preclinical work reached the clinic) | https://clinicaltrials.gov/data-api/api |

> **Status of `auto/`:** it is empty in this first commit. The environment that built the dataset could not reach these APIs (its network policy blocked them), so the curated file was assembled from cited web sources instead. The parsers in `tracker.py` were tested offline against mocked responses in the documented formats, but they have **not yet run against the live endpoints**. Expect small fixes on the first real run, especially the ClinicalTrials.gov query syntax and the Form D column names.

The curated `observations.csv` is updated by hand, or by asking Claude to re-research an indicator. Quarterly items (CRO bookings, vendor end-markets, VC and IPO totals) are best refreshed after each earnings season, in early February, May, August and November.

## How to read it

- **Lead-time ladder** (rough, from literature and vendor commentary; not yet back-tested):
  appropriations/policy (3–6 qtrs) → NIH award pace, S10 grants, biotech funding (2–4 qtrs) → CRO bookings, job postings, instrument orders (1–2 qtrs) → vendor revenue (0). Phase 1 starts *lag* preclinical work, so they confirm rather than lead.
- **Two-channel divergence matters.** In 2025–26 the academic channel (NIH) and the biopharma channel (CRO bookings, pharma R&D) have been moving in different directions. Read each channel separately before netting them.
- **Back-testing idea:** regress `TOOLS_REV_BASKET_Q_YOY` on the leading series at 1–6 quarter lags, once `auto/` is populated.

## Caveats

- VC totals differ a lot by publisher (PitchBook vs. HSBC vs. JLL definitions). Each series keeps one publisher, named in `source_name`, and different publishers use separate `indicator_id` suffixes.
- Vendor "academic & government" numbers are often global, not US-only, and often qualitative. `notes` says which.
- The M3 instrument category (NAICS 3345) also includes medical and industrial instruments, so it is a noisy proxy.
- Pharma XBRL R&D includes acquired IPR&D for some filers, which makes it lumpy.
- Some press-sourced figures are secondary reports of primary data. Where a primary source exists, prefer it on the next refresh.
