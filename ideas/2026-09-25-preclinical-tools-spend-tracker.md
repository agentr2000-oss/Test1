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

## Why it's interesting

Tools stocks and lab suppliers swing hard on funding cycles: the 2021 biotech boom, the 2023–24 hangover, and the 2025 NIH shock. The signals show up months earlier in appropriations, grant award pace, venture rounds, CRO bookings and vendor order books. A single tracker covering all three buyer groups should show inflection points before revenue does.

## Related

- Tracker, dataset and refresh script: [investment-research-workflow `trackers/preclinical_tools/`](https://github.com/agentr2000-oss/investment-research-workflow/tree/claude/test/trackers/preclinical_tools)
- NIH RePORTER (grant awards): https://reporter.nih.gov/
- Charles River DSA book-to-bill, the cleanest direct preclinical demand read: https://ir.criver.com/
- FRED instrument orders (Census M3, A34KNO): https://fred.stlouisfed.org/series/A34KNO
- SEC Form D data sets (private biotech raises): https://www.sec.gov/data-research/sec-markets-data/form-d-data-sets
