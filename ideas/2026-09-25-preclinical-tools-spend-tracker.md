# Preclinical Tools "Picks & Shovels" Spend Tracker

**Date:** 2026-09-25
**Category:** Research

## One-liner

A tracker of leading indicators for preclinical tools and equipment spend (the picks and shovels) across academic research, biotech and pharma R&D. It starts with the US.

## Notes

- I want to see where lab tools and equipment demand is heading *before* it shows up in vendor revenue.
- Three buyer groups feed preclinical tools spend:
  - **Academic research.** NIH and NSF money flows into grants, then lab budgets, then instruments and consumables.
  - **Biotech.** VC, IPO and follow-on money flows into hiring, then lab buildouts, then orders.
  - **Pharma R&D.** Budgets flow into internal discovery work and outsourced preclinical studies at CROs.
- The goal is *leading* indicators, not a rear-view mirror.
- Start with the US. Maybe expand to Europe and China later.
- First step: build the dataset. Done, and it now lives in the research repo: [`trackers/preclinical_tools/`](https://github.com/agentr2000-oss/investment-research-workflow/tree/claude/test/trackers/preclinical_tools) on `claude/test` of investment-research-workflow, with a dashboard, the [Preclinical Tools Monitor](https://claude.ai/artifact/Vm5GX93Kp5r1sWz3DmFAqS).
- New dashboard charts (2026-09-26):
  - **Documents that lead spending**, the paper trail that moves *before* the money shows up:
    - NIH and NSF funding notices
    - federal lab-equipment tenders and awards
    - NIH cash paid out by fiscal year
    - lab instrument imports
    - lab fit-out permits by city (Boston, SF, San Diego, Montgomery County MD, Seattle, Philly)
    - primate imports

    They stay hidden until the first `tracker.py fetch` pulls real data. The cloud session can't reach those sites.
  - **From data already in hand:**
    - vendor organic growth side by side (Waters +9% leads, Avantor −0.4% trails)
    - San Diego lab vacancy from four brokers (all 25–28% countywide)
    - Inotiv's preclinical backlog ($152m, rebuilding since late 2024)
    - NIH/NSF budget requests vs what Congress actually gave
- Private-side signals added (2026-09-28), since biotech and pharma money is where the upcycle is coming from:
  - **From filings** (they fill in on the next `tracker.py fetch`):
    - how many months of cash listed biotechs have left
    - new life-science VC funds on Form D
    - NIH small-business grants
    - H-1B filings for lab scientists
    - reagent and microscope imports
  - **Researched now** (all from search summaries, so still to be checked):
    - Early-stage money is thin: seed + Series A fell to $8.7bn in 2025 from $10.6bn, and most 2026 rounds went to companies already in the clinic. Citeline's drug pipeline shrank for the first time in ~30 years, led by fewer preclinical assets.
    - Hiring and lab space are turning up: BioSpace R&D job postings +42% y/y, Boston lab searches 28 → 49 companies in a quarter.
    - Work is moving to China: WuXi AppTec's backlog +25% vs about +2% for Charles River; China is ~32% of global licensing deal value.
  - **Watch:** OMB's first BIOSECURE list of restricted Chinese biotechs, due by Dec 18.
- Filings around preclinical work (2026-09-28). Preclinical studies themselves don't get filed anywhere until the IND at the end, so these read the paper trail around them:
  - **USDA animal-use reports:** these give a volume read on drug safety studies, since that's where most monkeys and dogs go.
    - Monkeys held or used in US research are roughly flat at ~105–114k a year (106k in FY2025).
    - Dogs slid from 48k to 42k, and rabbits from 146k to 109k (FY2021 → FY2025).
  - **Company filings that mention "IND-enabling" work:** counted from SEC full-text search each quarter. These fill in on the next `tracker.py fetch`.
  - **Patent applications in drug and biotech classes:** a slow read, since they publish ~18 months after filing.
    - US applicants' European filings fell ~10% in both pharma and biotech in 2025.
    - Global biotech PCT filings were −3.9%.
    - The monthly USPTO series needs a free PatentsView key.
  - All the researched numbers came from search summaries, so they're still to be checked.
- More leading indicators (2026-09-28), chosen because they move before money is committed:
  - **From filings** (they fill in on the next `tracker.py fetch`):
    - biotech 8-Ks mentioning strategic alternatives, layoffs, reverse mergers or at-the-market share sales (distress and fundraising)
    - first-time biotech S-1/F-1 registrations (the IPO pipeline)
    - ARPA-H awards
    - FDA orphan designations (needs a manual export from FDA's database first)
  - **Researched now** (all from search summaries, still to be checked):
    - Lab instruments are splitting: Illumina instruments +31% in Q2 2026, but 10x Genomics −47% and Bio-Rad Life Science −5% (Bio-Rad blames academic demand).
    - Alternatives to animal testing aren't taking off yet: Certara bookings +1%, Schrödinger software −10%.
    - Labcorp's book-to-bill is above 1 like Charles River's, but Chinese preclinical labs are booming (Joinn backlog +61%).
    - Why NIH success rates fell: more applications (R01 applications 37k → 42k) chasing the same money, and NCI's funding cutoff dropped to the 4th percentile.
  - **Couldn't get:** FDA pre-IND meeting counts, which only appear in PDF reports.

## Why it's interesting

Tools stocks and lab suppliers swing hard on funding cycles: the 2021 biotech boom, the 2023–24 hangover, and the 2025 NIH shock. The signals show up months earlier in appropriations, grant award pace, venture rounds, CRO bookings and vendor order books. A single tracker covering all three buyer groups should show inflection points before revenue does.

## Related

- Tracker, dataset and refresh script: [investment-research-workflow `trackers/preclinical_tools/`](https://github.com/agentr2000-oss/investment-research-workflow/tree/claude/test/trackers/preclinical_tools)
- NIH RePORTER (grant awards): https://reporter.nih.gov/
- Charles River DSA book-to-bill, the cleanest direct preclinical demand read: https://ir.criver.com/
- FRED instrument orders (Census M3, A34KNO): https://fred.stlouisfed.org/series/A34KNO
- SEC Form D data sets (private biotech raises): https://www.sec.gov/data-research/sec-markets-data/form-d-data-sets
- Daily Treasury Statement (NIH cash actually paid out): https://fiscaldata.treasury.gov/datasets/daily-treasury-statement/
- Grants.gov (NIH and NSF funding notices): https://www.grants.gov/
- Census trade data (primate and lab instrument imports): https://www.census.gov/data/developers/data-sets/international-trade.html
- SEC XBRL frames API (listed biotechs' cash and R&D): https://www.sec.gov/search-filings/edgar-application-programming-interfaces
- DOL H-1B disclosure data (lab scientist hiring): https://www.dol.gov/agencies/eta/foreign-labor/performance
- Early-stage biotech funding (J.P. Morgan via BioSpace): https://www.biospace.com/business/early-stage-biotechs-feel-the-squeeze-as-funding-favors-derisked-assets-jpm
- Citeline pipeline shrinking: https://www.biospace.com/drug-development/pharma-pipeline-stalls-for-first-time-in-decades-citeline
- China's share of licensing deals (Jefferies): https://www.fiercebiotech.com/biotech/china-biotechs-reshaping-us-biopharma-outlicensing-deals-rise-11-jefferies-report
- USDA animal-use summaries (research facility annual reports): https://www.aphis.usda.gov/awa/research-facility-report/annual-summary
- SEC EDGAR full-text search: https://www.sec.gov/edgar/search/efts-faq.html
- PatentsView patent search API: https://search.patentsview.org/docs/
- EPO patent filings from US applicants, 2025: https://www.prnewswire.com/news-releases/technology-dashboard-2025-us-remains-leading-country-of-origin-for-european-patent-applications-as-china-makes-gains-302722354.html
- FDA orphan designations database: https://www.accessdata.fda.gov/scripts/opdlisting/oopd/
- EDGAR quarterly form index (S-1 filings): https://www.sec.gov/Archives/edgar/full-index/
- Illumina Q2 2026 results: https://www.sec.gov/Archives/edgar/data/0001110803/000111080326000155/q226earningsrelease.htm
- 10x Genomics Q2 2026 results: https://www.sec.gov/Archives/edgar/data/1770787/000162828026054273/txg-20260806xexx991.htm
- Certara Q2 2026 results: https://www.sec.gov/Archives/edgar/data/1827090/000182709026000026/q22026earningsreleaseex99.htm
- NCI payline at the 4th percentile (Cancer Letter): https://cancerletter.com/cancer-policy/20250725_5a/
