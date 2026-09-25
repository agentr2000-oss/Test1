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
| Authority | NDAA and appropriations markups, CRs, OMB apportionments, reprogrammings | 3-12 mo |
| Market signals | SAM.gov RFIs / sources sought / presolicitations, agency acquisition forecasts, SBIR/DIU solicitations, DSCA arms-sale notifications, lobbying disclosures | 3-24 mo |
| Award | DoD daily contract announcements (same day), USAspending / SAM.gov awards (90-day DoD delay), IDIQ ceilings, OTAs | 0 (the target) |
| Cash | Daily Treasury Statement DoD cash withdrawals, Monthly Treasury Statement outlays | lagging/coincident |
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

Links checked 2026-09-25 against live search results. Most .gov hosts were blocked from direct fetch in the sandbox, so a few are marked ⚠. Lead times are rough guesses to be tested in backtests.

### US datasets

**Heads-up, lots of things moved in 2025-26:** defense.gov is now war.gov (Comptroller is now comptroller.war.gov); FPDS was shut down (Feb 2026), so use the SAM.gov Contract Awards API; new FMS notifications moved from DSCA to State (Feb 2026); lda.senate.gov retired (June 2026), so use lda.gov.

**Big structural trick:** DoD contract data in USAspending/FPDS is **delayed 90 days** for OPSEC. The daily contract announcements (≥$7.5M) are same-day, so they *lead* the official award data by ~3 months for free.

Pipeline / pre-award (leading)

| Source | Link | API | Signal | Lead |
|---|---|---|---|---|
| SAM.gov Contract Opportunities | [sam.gov/opportunities](https://sam.gov/opportunities) | [Opportunities API](https://open.gsa.gov/api/get-opportunities-public-api/) (key, 1k req/day) | Sources sought / RFIs / presolicitations, filter by DoD office + NAICS/PSC | RFIs ~6-18 mo; presol ~1-3 mo |
| DoD component acquisition forecasts | [DoD OSBP forecasts (archived)](https://business.defense.gov/Archived-Pages/Acquisition-Forecasts/), [Air Force](https://www.airforcesmallbiz.af.mil/Small-Business/Acquisition-Forecasts/), [DLA demand forecast](https://www.dla.mil/Acquisition/Industry-Engagement-and-Analysis/Demand-Forecast/) | – | Planned buys by component | 6-24 mo |
| GSA Acquisition Gateway forecast | [acquisitiongateway.gov/forecast](https://acquisitiongateway.gov/forecast) | none yet | ⚠ DoD reportedly doesn't participate (civilian agencies only) | – |
| DoD budget (P-1 / R-1 / FYDP) | [comptroller.war.gov/Budget-Materials](https://comptroller.war.gov/Budget-Materials/) | – | Program-level request, 5-yr FYDP | 6-18 mo (FYDP 1-5 yrs) |
| DoD reprogrammings | [Reprogramming FY2026](https://comptroller.war.gov/Budget-Execution/ReprogrammingFY2026/) | – | Money being moved mid-year, clusters at FY-end | weeks-3 mo |
| OMB apportionments | [apportionment-public.max.gov](https://apportionment-public.max.gov/), [OpenOMB](https://openomb.org/) | – | OMB must approve before DoD can obligate; posted within 2 days, footnotes show holds | days-weeks |
| Congress.gov (NDAA / approps) | [api.congress.gov](https://api.congress.gov/) | [docs](https://github.com/LibraryOfCongress/api.congress.gov) | Marks, bill status, plus-ups | 3-12 mo |
| Lobbying (LDA) | [lda.gov](https://lda.gov/system/public/) | [lda.gov/api/v1](https://lda.gov/api/redoc/v1/) | Issue codes DEF/BUD, bill mentions | weak, 6-18 mo |
| Foreign Military Sales notifications | [State Dept (current)](https://www.state.gov/arms-sales-congressional-notifications), [DSCA archive](https://www.dsca.mil/Press-Media/Major-Arms-Sales) | also in Federal Register | Proposed foreign sales | LOA 1-12 mo; contracts 6-24 mo |
| SBIR/STTR | [sbir.gov/api](https://www.sbir.gov/api), [DoD topics](https://www.dodsbirsttr.mil/topics-app/) | yes | Topic counts by tech area (new topics monthly) | 4-9 mo |
| DIU / AFWERX | [DIU open solicitations](https://www.diu.mil/work-with-us/open-solicitations), [AFWERX SBIR](https://afwerx.com/divisions/sbir-sttr/) | – | Rapid-prototype demand | 2-4 mo |
| Federal Register | [federalregister.gov](https://www.federalregister.gov/) | [API v1](https://www.federalregister.gov/developers/documentation/api/v1) (no key) | DFARS rules, arms-sale notices | weeks-months |

Award / cash (coincident: the thing we're predicting)

| Source | Link | API | Notes |
|---|---|---|---|
| DoD daily contract announcements | [war.gov/News/Contracts](https://www.war.gov/News/Contracts/) | scrape | Same day, ≥$7.5M, leads USAspending by ~90 days |
| USAspending | [usaspending.gov](https://www.usaspending.gov/) | [api.usaspending.gov](https://api.usaspending.gov/docs/endpoints) | Awards, IDV ceilings vs obligations (headroom!), subawards. DoD delayed 90 days |
| SAM.gov Contract Awards (FPDS replacement) | – | [Contract Awards API](https://open.gsa.gov/api/contract-awards/) | Same 90-day DoD delay |
| Daily Treasury Statement | [fiscaldata DTS](https://fiscaldata.treasury.gov/datasets/daily-treasury-statement/) | [API docs](https://fiscaldata.treasury.gov/api-documentation/) | Daily DoD cash withdrawals, T+1. ⚠ line appears as "Dept of Defense (DoD) - misc" now (was "Defense Vendor Payments (EFT)"), so check the exact `transaction_catg` |
| Monthly Treasury Statement | [fiscaldata MTS](https://fiscaldata.treasury.gov/datasets/monthly-treasury-statement/) | same | Monthly DoD outlays |
| GAO bid protests | [gao.gov bid protest search](https://www.gao.gov/legal/bid-protests/search) | – | Protest spikes = big awards landing; delays award up to 100 days |
| GAO Weapon Systems Assessment | [GAO-26-108457](https://www.gao.gov/products/gao-26-108457) | – | Annual program health |

Macro / industry

| Source | Link | Notes |
|---|---|---|
| Census M3 defense capital goods | FRED [ADEFNO](https://fred.stlouisfed.org/series/ADEFNO) (new orders), [ADEFUO](https://fred.stlouisfed.org/series/ADEFUO) (backlog), [ADEFVS](https://fred.stlouisfed.org/series/ADEFVS) (shipments), [ADAPNO](https://fred.stlouisfed.org/series/ADAPNO) (defense aircraft orders) | Monthly, ~18 working days after month-end. Orders lead shipments |
| Fed industrial production: defense & space | FRED [IPB52300S](https://fred.stlouisfed.org/series/IPB52300S) | Monthly |
| Shipbuilding jobs | FRED [CES3133660001](https://fred.stlouisfed.org/series/CES3133660001) | Hiring leads shipments 1-3 qtrs |
| SEC EDGAR | [EDGAR APIs](https://www.sec.gov/search-filings/edgar-application-programming-interfaces), [full-text search](https://efts.sec.gov/LATEST/search-index?q=%22munitions%20capacity%22) | Prime backlog / RPO, 8-K contract wins; supplier text mining ("undefinitized", "multiyear", "book-to-bill") |
| SIPRI | [Milex DB](https://www.sipri.org/databases/milex), [Arms Transfers DB](https://armstransfers.sipri.org/) | Annual, lagging, for context |
| Cleared jobs | [ClearanceJobs hiring trends](https://about.clearancejobs.com/employers/learn-more/hiring-trends) | ⚠ reports only, no public dataset |
| GDELT / ACLED (drivers) | [GDELT data](https://www.gdeltproject.org/data.html), [ACLED API](https://acleddata.com/acled-api-documentation) | Conflict and event signals behind supplementals and FMS |
| Satellite imagery | [Copernicus Data Space APIs](https://dataspace.copernicus.eu/analyse/apis) | Free Sentinel-1/2 of ammo plants (Holston, Radford, Scranton, Mesquite) and shipyards. Cross-check against the MILCON budget |

US context right now (Sept 2026): the House passed the FY27 NDAA (H.R. 8800) on 7/22 and the Senate bill is stalled, so a CR (and its new-start limits) looks likely. SBIR lapsed from 10/1/2025 to 4/13/2026 (P.L. 119-83), so SBIR data in that window is depressed.

### India datasets

_India links still being verified, to be added._
