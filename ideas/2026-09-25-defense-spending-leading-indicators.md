# Defense Spending Leading Indicators Tracker (US + India pilot)

**Date:** 2026-09-25
**Category:** Research

## One-liner

Defense money is opaque at the point it's spent, but it leaves a paper trail upstream. So build a tracker that watches the top of the procurement funnel (budget intent, approvals, RFIs, lobbying, hiring) to see contracts and spending coming months or years before they land. Pilot it on the US and India.

## Notes

Original ask: brainstorm how to build a tracker of leading indicators for defense spending / defense contracts. Are there clever ways to do it, given this stuff tends to be quite opaque? Try the US as a pilot, and India as well. Look for interesting datasets that give good leading indicators.

### The core trick: treat it as a funnel with lags

Nobody publishes "what the military will buy next quarter." But every rupee and dollar goes through a fixed sequence of public-ish steps. Each step has a dataset. So:

1. Map each country's procurement pipeline stage by stage.
2. Find a dataset for each stage.
3. Measure the **lag** and the **conversion rate** between stages from past data (e.g. "India AoN approvals turn into signed contracts ~X% of the time, after Y months").
4. The tracker then reads the top of the funnel today and projects what comes out the bottom.

```
Drivers → Intent → Authority/Approval → Market signals → Award → Cash → Industry
(threats)  (budget)  (NDAA / DAC AoN)    (RFIs, tenders)  (contracts) (outlays) (backlog, orders)
  LEADING ─────────────────────────────────────────────────────────────────────► LAGGING
```

### US funnel (pilot #1)

| Stage | What to watch | Rough lead |
|---|---|---|
| Drivers | Conflict/geopolitical event data (GDELT, ACLED), supplemental requests | 6-24 mo |
| Intent | President's Budget, FYDP out-years, P-1/R-1 line items, Unfunded Priorities Lists | 12-24 mo |
| Authority | NDAA and appropriations markups, CRs, reprogrammings | 3-12 mo |
| Market signals | SAM.gov RFIs / sources sought / presolicitations, agency acquisition forecasts, SBIR/DIU solicitations, DSCA arms-sale notifications, lobbying disclosures | 3-24 mo |
| Award | USAspending / FPDS, DoD daily contract announcements, IDIQ ceilings, OTAs | 0 (the target) |
| Cash | Daily Treasury Statement defense vendor payments, Monthly Treasury Statement outlays | lagging/coincident |
| Industry | Census M3 defense capital goods orders, Fed industrial production (defense & space), prime backlog / book-to-bill | coincident |

### India funnel (pilot #2)

| Stage | What to watch | Rough lead |
|---|---|---|
| Drivers | Border incidents / conflict (e.g. post-Operation Sindoor emergency buys) | 3-24 mo |
| Intent | Union Budget MoD capital outlay (BE vs RE), Standing Committee on Defence "projected vs allocated" gaps | 12+ mo |
| Approval | Defence Acquisition Council (DAC) Acceptance of Necessity (AoN) approvals, Cabinet Committee on Security clearances | 1-5 yrs (!) |
| Market signals | Tenders/RFPs on the MoD e-procurement portal and CPPP, GeM, iDEX challenges, Positive Indigenisation Lists (SRIJAN) | 6-36 mo |
| Contract | MoD contract-signing press releases, DPSU/listed-company order-win filings on BSE/NSE | 0 (the target) |
| Cash | Controller General of Accounts monthly accounts (defence capex) | lagging/coincident |
| Industry | DPSU order books (HAL, BEL, BDL, Mazagon, GRSE, Cochin...), defence production and export stats, Nifty India Defence index | coincident |

### Clever / non-obvious angles

- **AoN → contract conversion rate (India).** DAC approves huge rupee numbers, but only some of it gets contracted, and years later. Text-mine every PIB DAC release into a dataset (date, ₹ value, platform, service, Buy category), then match to later contract signings. The "unconverted AoN backlog" is basically a future-orders pipeline.
- **IDIQ ceiling headroom (US).** Ceiling minus obligated-to-date on big IDIQ vehicles = pre-authorised spend waiting to be drawn down as task orders.
- **Sources-sought / RFI counts by NAICS (US).** e.g. 336414 guided missiles, 332993 ammunition, 336611 shipbuilding. A spike in RFIs in a category comes before the awards.
- **Foreign Military Sales notifications.** DSCA notifies Congress of proposed sales well before the LOA and contracts, so it's a clean export-demand lead.
- **Sub-award data.** FFATA subawards in USAspending show who's getting money *under* the primes, i.e. the supply chain ramping.
- **Supplier chatter.** NLP on Tier-2/3 supplier earnings calls and filings (castings, energetics, electronics) for "defense" mentions and capacity adds. They see demand before the primes' numbers move.
- **Hiring.** Cleared-job postings in the US; DPSU / shipyard recruitment notices in India.
- **Physical signals.** Satellite imagery (Sentinel-2 is free) of shipyards and ammo plants, e.g. new buildings, dry dock activity, parking lot fill.
- **Language shift.** Track words like "urgent", "surge", "emergency procurement" or "rapid" in solicitations and press releases as a regime-change flag.
- **Bid protests (US).** A spike in GAO protests in a category means large competitive awards were just made or are about to be re-made.
- **Parliament Q&A (India).** Lok Sabha / Rajya Sabha answers often reveal contract status, delays and trial stages that aren't announced anywhere else.

### Gotchas

- **Seasonality is huge.** US fiscal-year-end (September) "use it or lose it" spike; India's March year-end rush. Need to seasonally adjust or everything looks like a signal.
- **Headline vs. real money.** US IDIQ ceilings and India AoN values are *potential* spend, not actual. They're heavily inflated, so conversion rates matter more than headline numbers.
- **Classified / black budget.** Some US spending just won't show up. Track the unclassified part and treat the gap as a known unknown.
- **India data is messy.** It's mostly PIB press releases, PDFs and exchange filings, not APIs. Expect a lot of scraping and LLM extraction ("pull rupee value, platform, service, vendor out of this press release").
- **Continuing resolutions (US)** delay new-start programs, which breaks lag assumptions in CR years.

### MVP sketch

- Pick 4-5 signals per country that are easy to pull (US: SAM.gov opportunities, USAspending, Daily Treasury Statement, DSCA notifications, M3 defense orders; India: PIB DAC/AoN releases, CGA monthly capex, DPSU order-win filings, defproc tenders, Standing Committee reports).
- Weekly scraper → SQLite/DuckDB → simple dashboard.
- Backtest: does signal X lead obligations/outlays Y? (cross-correlation / lead-lag, maybe Granger). Keep the ones that actually lead.
- LLM layer to turn unstructured press releases and filings into rows (value, platform, service, vendor, stage).

## Why it's interesting

- Defense budgets are rising fast in a lot of countries, and everyone (investors, suppliers, analysts, journalists) wants to know where the money goes *next*, not where it went.
- The data is out there, it's just scattered and unstructured. The edge comes from stitching the stages together and measuring the lags, which nobody does well for free (Govini, HigherGov and GovTribe cover pieces of this for the US, mostly behind paywalls).
- India is especially interesting: huge import-to-indigenisation shift, big DAC approval numbers, and a very visible gap between "approved" and "contracted." A conversion-rate tracker there could be really useful.
- The US/India pair is a nice test: one country with great structured data (so we can validate the method), one with messy data (to see whether the method still works).

## Related

_Dataset links being verified — to be added._
