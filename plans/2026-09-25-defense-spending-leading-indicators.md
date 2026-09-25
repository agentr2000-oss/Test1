# Defense Spending Leading Indicators Tracker — Plan

**Date:** 2026-09-25
**Idea:** [Link to original idea](../ideas/2026-09-25-defense-spending-leading-indicators.md)
**Status:** Draft

## Problem Statement

Defense spending is hard to see at the point the money is spent, but it leaves a public trail upstream: budget requests, approvals, RFIs, contract announcements, cash outflows. The trouble is that each piece sits in a different place and format. Nobody stitches the stages together or measures **how long each stage takes and how much gets through**, so there's no good free way to see contracts coming before they land.

Who has this problem: people who care where defense money goes *next*. That means investors in defense names (Indian DPSUs, US primes and their suppliers), suppliers doing business development, and analysts or journalists covering procurement.

It's especially sharp in India. The Defence Acquisition Council's "Acceptance of Necessity" (AoN) approvals are big headline numbers (₹6.81 lakh cr in FY26), but only about a third of that turned into contracts that year, and individual items can take 2-5+ years. Nobody publishes an AoN-to-contract conversion rate. In the US the data is better structured, but DoD award data is held back 90 days, and the free same-day source (the daily contract announcements) is unstructured prose.

## Proposed Approach

**Start narrow with two "wedge" datasets** that are useful on their own, buildable in a few weeks, and don't exist in clean, free form today:

1. **India AoN ledger.** Every DAC approval since ~2018 as structured rows, matched to later contract signings. That gives conversion rates, lag distributions and an "unconverted AoN backlog" (the pipeline of future orders).
2. **US daily contracts feed.** A scraper and parser for DoD's same-day contract announcements (≥$7.5M), turned into structured rows and later reconciled against USAspending once the 90-day delay passes.

Then **test whether they actually lead anything** (DPSU order inflow and government capex in India; DoD obligations, outlays and defense capital goods orders in the US). Only after that, add the next signals from the idea file.

Design principles:
- **Keep the source text for every row.** Every row links to the page it came from, and the raw HTML/PDF is cached. The numbers disagree between releases, so being able to trace a figure back matters.
- **Regex first, LLM second.** Parse with rules where the text is formulaic. Use an LLM with a strict JSON schema for the messy parts, and send anything low-confidence to a review queue instead of guessing.
- **Boring stack.** Python + DuckDB/Parquet in the repo, a scheduled GitHub Actions job to refresh, and a markdown digest before any dashboard.

## Key Components

- **Phase 0: Skeleton (a few days).** Repo layout (`scrapers/`, `parsers/`, `data/raw/`, `data/clean/`, `analysis/`), a polite HTTP fetcher with caching and rate limits, a DuckDB file, and an LLM extraction helper (JSON schema in, validated rows out, confidence score, source span).

- **Phase 1: US daily contracts feed (1-2 weeks).**
  - Scrape the [war.gov/News/Contracts](https://www.war.gov/News/Contracts/) archive back as far as it goes (aim for ~2015+).
  - Split each day's page into one paragraph per award and parse it into: `date, service/agency, company, location, value, contract_number, contract_type, modification?, funds_obligated, completion_date, contracting_activity, is_fms, fms_countries, description`.
  - Classify each award into a small set of buckets (munitions, shipbuilding, aircraft, space, C4ISR/cyber, services...). Use keywords/LLM now, and later swap in the NAICS/PSC codes from USAspending once the award can be matched.
  - **Reconcile:** after 90 days, match on contract number (PIID) against [USAspending](https://api.usaspending.gov/docs/endpoints) to check values and pull in industry codes.
  - Output: a daily table plus a weekly "what got awarded" summary by bucket and service.
  - Done when: ≥95% of paragraphs parse with company + value + contract number, and ≥90% match USAspending after the delay.

- **Phase 2: India AoN ledger (2-3 weeks — the matching is the hard part).**
  - **Collect.** Every DAC and CCS release from PIB/MoD (the [PIB archive by ministry](https://archive.pib.gov.in/archive/phase2/archiveministry.aspx), [MoD press releases](https://mod.gov.in/press-releases-ministry-defence)) plus MoD "contract signed" releases. Add BSE order-win and "L1"/Letter of Intent filings for HAL, BEL, BDL, Mazagon, GRSE, Cochin, BEML, Solar and Data Patterns ([BseIndiaApi](https://github.com/BennyThadikaran/BseIndiaApi)).
  - **Extract.** Two tables:
    - `aon_meeting`: date, total ₹, number of proposals, share indigenous
    - `aon_item`: meeting, platform/system, service, DAP category (e.g. Buy Indian-IDDM), quantity, ₹ if given
    - `contract`: date, platform, vendor, ₹, service, source (PIB / BSE), plus an optional link to an AoN item
  - **Match.** Connect each contract to its AoN item. Start with candidates on platform + service + time window, then have an LLM judge "same programme?" (names drift, e.g. "P-75I" vs "six conventional submarines"). Anything below a confidence threshold goes to a small manual review CSV.
  - **Metrics.** Conversion rate (₹ and count) by year, service and category; lag distribution from AoN to contract; open AoN backlog over time.
  - Done when: FY22-FY26 AoNs are fully in the ledger, and the ledger's yearly contract totals come within ~10% of MoD's published figures.

- **Phase 3: Do these actually lead? (1-2 weeks).**
  - **US.** Does weekly award value by bucket lead the official obligations in USAspending, daily DoD cash in the [Daily Treasury Statement](https://fiscaldata.treasury.gov/datasets/daily-treasury-statement/), or FRED [ADEFNO](https://fred.stlouisfed.org/series/ADEFNO)/[ADEFUO](https://fred.stlouisfed.org/series/ADEFUO) (new and unfilled orders for defense capital goods)?
  - **India.** Does the open AoN backlog lead DPSU order inflow (from quarterly filings) and Controller General of Accounts defence capex?
  - Method: seasonally adjust first (US September and India March year-end spikes), then look at lead-lag cross-correlation and a simple out-of-sample check. Expect small samples in India, so present ranges, not point forecasts.

- **Phase 4: Tracker output + next signals (ongoing).**
  - A weekly markdown digest committed to the repo, covering new awards, new AoNs, conversions, backlog and anything unusual. A small dashboard comes later, if it proves useful.
  - Add the next signals in order of value/effort:
    1. BSE "L1"/LoI keyword alerts
    2. SAM.gov sources-sought counts by industry code (NAICS)
    3. State Dept/DSCA arms-sale notifications
    4. OMB apportionments
    5. Standing Committee "committed liabilities"

## Resources Needed

- **Skills:** Python scraping and parsing, basic time-series work, and some fluency in Indian procurement jargon (DAP categories, AoN → RFP → trials → CNC → CCS) and US contract types (IDIQ, FFP, cost-plus, mods, FMS).
- **Tools (all free):** Python (httpx, BeautifulSoup, pandas, DuckDB), GitHub Actions for scheduled scrapes, and a free [SAM.gov API key](https://open.gsa.gov/api/get-opportunities-public-api/) for later phases. USAspending, FRED and Treasury need no key (FRED's API needs one, but its CSV download doesn't).
- **LLM for extraction and matching:** a small, cheap model (e.g. Claude Haiku 4.5) for bulk extraction, and a bigger one only for tricky matches. Cost should be modest at this volume (thousands of pages, not millions), but estimate it on a 100-page pilot before running the full archive.
- **Network access:** this cloud environment's network policy blocked most .gov hosts (war.gov, pib.gov.in, mod.gov.in, fiscaldata.treasury.gov...) during research. To build the scrapers here, allow those domains under Network access in the environment settings (see the [Claude Code on the web docs](https://code.claude.com/docs/en/claude-code-on-the-web)). Otherwise, run the scrapers from a laptop or GitHub Actions.
- **Time:** evenings/weekends pace. Roughly 5-8 weeks to get through Phase 3, with Phase 2 matching the most uncertain part.

## Open Questions

- [ ] **Do DAC releases give ₹ values per item, or only a total per meeting?** If only totals, item-level conversion needs values from contract releases, and the ₹ conversion rate stays at meeting/year level.
- [ ] How far back is the PIB/MoD archive usable, and did the release format change (HTML vs PDF, Hindi-only releases)?
- [ ] How good can AoN → contract matching get? What share will end up in manual review, and how much of that am I willing to hand-label?
- [ ] Does the war.gov contracts archive go back cleanly past the defense.gov → war.gov move, or do old URLs need separate handling?
- [ ] What's the India target variable: DPSU order inflow, CGA capex (if it breaks out defence at all), or MoD's annual "contracts signed"?
- [ ] What's the US target variable: USAspending obligations, Daily Treasury Statement outlays, or ADEFNO? Probably test all three.
- [ ] Who is this for — my own investing/research, a newsletter, or a product? That shapes Phase 4 and how much polish matters.
- [ ] Scraping etiquette: robots.txt and terms of use for war.gov, PIB, BSE; keep request rates low and cache everything.

## Next Steps

1. **Parse one month of US contract announcements.** Pull ~20 days of [war.gov/News/Contracts](https://www.war.gov/News/Contracts/) pages, write the paragraph splitter plus regex parser, and measure how many parse cleanly. That shows how much the LLM layer needs to do.
2. **Hand-build the 2026 India AoN rows.** Take the four 2026 DAC releases (12 Feb, 27 Mar, 3 Jul, 7 Sep), fill in the `aon_meeting`/`aon_item` schema by hand, and answer the "per-item ₹ values?" question. That settles the ledger design before any scraping.
3. **Decide the audience** (just me vs. newsletter vs. product) and set up the repo skeleton + GitHub Actions job so the first scraper has somewhere to live.
