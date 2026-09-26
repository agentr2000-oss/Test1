# US Preclinical Tools Spend: Leading Indicators Dataset

A cited, refreshable dataset of **leading indicators for US preclinical "picks and shovels" spend**: lab instruments, consumables, research models and outsourced preclinical studies. It covers the three buyer groups that fund that spend:

| Buyer group | Money trail | Where it shows up first |
|---|---|---|
| **Academic & government** | Appropriations → NIH/NSF grant awards → lab budgets → instruments and consumables | NIH budget, award pace, S10 instrument grants, IDC policy |
| **Biotech** | VC, IPOs and follow-ons → hiring → lab buildouts → orders | Venture $, IPO window, XBI, layoffs, lab vacancy, Form D |
| **Pharma R&D** | R&D budgets → internal discovery + outsourced preclinical studies | Big-pharma R&D spend, Charles River DSA bookings |

Tools-vendor readouts (end-market growth, orders, guidance) and a few macro series (instrument orders, R&D hiring, rates) sit alongside. Vendor revenue is included as the **outcome** the leading indicators should predict.

_Started 2026-09-25. Idea note: [`ideas/2026-09-25-preclinical-tools-spend-tracker.md`](../../ideas/2026-09-25-preclinical-tools-spend-tracker.md)._

## Current read (as of 2026-09-25)

**Net: an early upcycle led by biopharma, with academia lagging.** Leading indicators on the biotech and CRO side turned up 2–3 quarters ago. Vendor orders are now accelerating. NIH-funded academic demand has stopped falling but has not recovered. Expect consumables to improve first. Instruments tied to new lab fit-outs follow later, more likely in 2027.

| Channel | Signal | Evidence (latest) |
|---|---|---|
| Preclinical CRO | 🟢 Turned up | Charles River DSA net book-to-bill **1.19x** in Q2 2026, the third straight quarter above 1x, after 0.82x in Q2–Q3 2025. Backlog **$1.97bn**, up from $1.80bn but still far below the $3.15bn 2022 peak. DSA organic revenue just turned positive (+0.2%). [Q2 2026 release](https://www.sec.gov/Archives/edgar/data/0001100682/000110068226000115/crl2q26earningsrelease.htm) |
| Biotech capital | 🟢 Turned up | PitchBook biopharma VC **>$10bn** in Q2 2026 vs $5.4bn in Q2 2025 ([PitchBook](https://pitchbook.com/news/reports/q2-2026-biopharma-report-funding-tops-10-billion-with-record-exits)). **$20bn** of follow-ons in H1 2026 (global, [DealForma](https://dealforma.com/biopharma-therapeutics-and-platforms-ipo-activity-follow-ons-and-pipes-q2-2026-review/)). XBI **+83%** over 12 months ([StockAnalysis](https://stockanalysis.com/etf/xbi/)). Layoff rounds **17** in Q2 2026 vs 64 a year earlier ([Fierce](https://www.fiercebiotech.com/biotech/biotechs-better-position-avoid-workforce-reductions-layoffs-continue-drop-q226)). |
| Biotech capital (caveat) | 🟡 Skewed late-stage | About 76% of H1 2026 VC dollars came in megarounds, mostly to clinical-stage companies ([BioPharma Dive](https://www.biopharmadive.com/news/biotech-venture-capital-funding-2026-first-half/824881/)). The seed share of deals hit a record-low 14% ([PitchBook](https://pitchbook.com/news/reports/q3-2025-biopharma-vc-trends)). Lab vacancy is still high: Boston **28.7%**, Bay Area **31.1%** ([CBRE](https://www.cbre.com/insights/figures/boston-metro-life-science-figures-q2-2026)). |
| Tools vendors | 🟢 Orders leading | Bruker's instrument-segment (BSI) bookings **+10%** in Q2 2026 ([8-K](https://www.sec.gov/Archives/edgar/data/0001109354/000119312526331511/brkr-ex99_1.htm)). Agilent instrument book-to-bill **≥1 for 10 quarters** ([call](https://finance.yahoo.com/markets/stocks/articles/agilent-technologies-q3-earnings-call-230418624.html)). Pharma end-market: Agilent **+12%**, Waters low double digits. FY2026 guides were raised at Thermo Fisher, Agilent, Waters and Revvity. |
| Academic & government | 🟡 Flat dollars, fewer grants | FY2026 NIH program level **~$47.5bn (+1.0%)** ([CRS](https://www.congress.gov/crs_external_products/R/PDF/R43341/R43341.58.pdf)). RPG success rate **21.3% → 18.5% → 13.0%** over FY23–FY25 ([NIH Data Book via DrugMonkey](https://drugmonkey.wordpress.com/2026/03/18/nih-finally-releases-some-fy2025-success-rate-data/)). Only **69%** of the FY26 extramural grant budget was obligated by Jul 31, and competitive awards are **−18%** vs FY24 ([AAMC](https://www.aamc.org/about-us/mission-areas/biomedical-research/publication/tracking-nih-awards-fy-2026-1)). That points to back-loaded Aug–Sep ordering. |
| Academic (vendor view) | 🟡 Bottoming, US uneven | Thermo Fisher A&G grew low single digits in Q2 2026, its first positive quarter in the series. Revvity US A&G was positive for the first time since mid-2023. But Bruker says US academic demand is "still soft", and Agilent A&G was −3%. |
| Academic policy | 🟡 Tail risk | The 15% indirect-cost cap is permanently enjoined and the appeal was dropped in Apr 2026 ([STAT](https://www.statnews.com/2026/04/08/trump-administration-drops-nih-indirect-costs-court-challenge/)). The FY27 request (**$41.4bn**, −13%) revives the cap. FY27 runs on a CR to **Dec 11, 2026** ([CRS](https://www.congress.gov/crs-product/R49353)). |
| Pharma R&D | ⚪ Not yet populated | Quarterly R&D for 10 big pharmas fills in on the first `tracker.py fetch` (SEC XBRL). |

**Upcoming catalysts:**
- Q3 earnings in late Oct / early Nov:
  - Can Charles River DSA book-to-bill hold above 1x?
  - Bruker US academic bookings: the test of the promised 2H26 recovery.
  - Thermo Fisher A&G.
- End-of-FY2026 NIH obligation data (October).
- PitchBook Q3 2026 biopharma VC (October).
- The FY27 CR deadline (Dec 11).

### Known gaps and low-confidence items

- **Not yet collected:** the research pass hit a web-search cap before reaching these. `python tracker.py check` lists every empty indicator.
  - NIH S10 annual totals, NSF budget, and the HERD university R&D and equipment series.
  - PhRMA R&D and 2025–26 pharma onshoring pledges.
  - The FDA/NIH animal-testing (NAMs) event log and FDA IND counts.
  - Inotiv book-to-bill; Bio-Techne, Mettler-Toledo and Avantor readouts; Danaher before Q2 2026.
  - San Diego lab vacancy and the count of biotechs trading below cash.
- **Conflicts kept side by side** (preferred source listed first):
  - FY2026 NIH ($47.49bn CRS vs $47.2bn Science).
  - FY2027 request ($41.4bn vs $41.2bn).
  - FY2027 House mark ($47.4bn vs $47.3bn).
  - 2023 biotech IPO count.
  - CBRE US lab vacancy for Q1 2026.
- **Flagged in `notes`:**
  - "LOW CONFIDENCE" or "attribution unverified" rows: some IPO, M&A and lab-vacancy figures, and the SynBioBeta series, which is not comparable with biopharma VC.
  - Figures that came only from transcripts or aggregators.
  - Replace these with primary sources on the next refresh.

## Files

| File | What it is |
|---|---|
| [`indicators.csv`](indicators.csv) | **Catalog.** One row per indicator: channel, signal role (leading / coincident / confirming / structural / target), typical lead time, how to read it (`higher = bullish` etc.), frequency, unit, series reference, source and access (free/paid). |
| [`observations.csv`](observations.csv) | **Curated data**, researched and cited row by row: budgets, grant stats, VC and IPO totals, CRO bookings, pharma R&D, vendor end-market commentary, policy events. |
| `auto/*.csv` | **API-refreshed data** from `tracker.py fetch`: FRED, NIH RePORTER, SEC XBRL, SEC Form D and ClinicalTrials.gov. Same columns as `observations.csv`. |
| [`latest.csv`](latest.csv) | Newest reading per indicator, with the prior reading and the change. Rebuilt by `tracker.py latest`. The change column is mechanical (same unit, prior period), so check `notes` when a definition changes. `rows_same_period > 1` flags conflicting sources for the same period. |
| [`tracker.py`](tracker.py) | Refresh / validate / summarize script. Python 3.9+, standard library only. |
| [`dashboard/`](dashboard/) | **Preclinical Tools Monitor**: a one-page dashboard built from the CSVs (scorecard, channel charts, vendor heatmaps, policy log, searchable indicator table). Rebuild with `python dashboard/build_dashboard.py` after `tracker.py latest`. The published copy is [on claude.ai](https://claude.ai/artifact/Vm5GX93Kp5r1sWz3DmFAqS) (private to you until shared). |

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
