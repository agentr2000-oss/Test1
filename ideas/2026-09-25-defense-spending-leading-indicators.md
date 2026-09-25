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
| Intent | Union Budget MoD capital outlay (BE vs RE), Standing Committee on Defence "projected vs allocated" gaps and % already committed | 12+ mo |
| Approval | Defence Acquisition Council (DAC) Acceptance of Necessity (AoN) approvals, Cabinet Committee on Security clearances | 1-5 yrs (!) |
| Market signals | Army/Navy/IAF RFIs, tenders on the MoD e-procurement portal and CPPP, iDEX challenges, Positive Indigenisation List embargo dates (SRIJAN), "L1 bidder" / LoI exchange filings | weeks-36 mo |
| Contract | MoD contract-signing press releases, DPSU/listed-company order-win filings on BSE/NSE, GeM orders | 0 (the target) |
| Cash | Controller General of Accounts monthly accounts (defence capex) | lagging/coincident |
| Industry | DPSU order books (HAL, BEL, BDL, Mazagon, GRSE, Cochin...), defence production and export stats, Nifty India Defence index | coincident |

### Clever / non-obvious angles

- **AoN → contract conversion rate (India).** DAC approves huge rupee numbers, but only some of it gets contracted, and years later. Text-mine every PIB DAC release into a dataset (date, ₹ value, platform, service, Buy category), then match to later contract signings. The "unconverted AoN backlog" is basically a future-orders pipeline.
- **"L1 bidder" filings (India).** Listed defence companies file to BSE/NSE when they're declared lowest bidder or get a Letter of Intent, weeks to months before the contract is signed. A simple keyword filter on exchange announcements ("L1", "Letter of Intent", "lowest bidder") could be a near-free early-warning feed.
- **Budget already committed (India).** The Standing Committee reports show how much of each service's capital budget is already locked in by past contracts (e.g. the Navy had ~74% committed for FY27). When that share is high, there's little room for new contracts that year; when it drops, new signings can open up.
- **DPSU management guidance.** BEL, HAL and others guide on order *inflow* for the next 1-2 years in earnings calls. It's management's own view of the pipeline, so track guidance vs. what actually lands.
- **The 90-day DoD delay (US).** Official DoD award data is held back 90 days, but the daily contract announcements are same-day. Scraping those gives you a 3-month head start over anyone relying on USAspending.
- **OMB apportionments (US).** Money can't be obligated until OMB approves how it's released, and those approvals are posted publicly within ~2 days. That's especially useful right after a CR ends or a bill is enacted.
- **IDIQ ceiling headroom (US).** Ceiling minus obligated-to-date on big IDIQ vehicles = pre-authorised spend waiting to be drawn down as task orders.
- **Sources-sought / RFI counts by NAICS (US).** e.g. 336414 guided missiles, 332993 ammunition, 336611 shipbuilding. A spike in RFIs in a category comes before the awards.
- **Foreign Military Sales notifications.** State/DSCA notify Congress of proposed sales well before the LOA and contracts, so it's a clean export-demand lead. It also works as a cross-country signal: US notices for India (Javelin, Excalibur, etc.) are an India import lead.
- **Sub-award data.** FFATA subawards in USAspending show who's getting money *under* the primes, i.e. the supply chain ramping.
- **Supplier chatter.** NLP on Tier-2/3 supplier earnings calls and filings (castings, energetics, electronics) for "defense" mentions and capacity adds. They see demand before the primes' numbers move.
- **Hiring.** Cleared-job postings in the US; DPSU / shipyard recruitment notices in India.
- **Physical signals.** Satellite imagery (Sentinel-2 is free) of shipyards and ammo plants, e.g. new buildings, dry dock activity, parking lot fill.
- **Language shift.** Track words like "urgent", "surge", "emergency procurement" or "rapid" in solicitations and press releases as a regime-change flag.
- **Bid protests (US).** A spike in GAO protests in a category means large competitive awards were just made or are about to be re-made.
- **Trials → orders (India).** DRDO tech transfers and PIB "successfully flight-tested" releases come 1-3 years before production orders.
- **Parliament Q&A (India).** Lok Sabha / Rajya Sabha answers often reveal contract status, delays and trial stages that aren't announced anywhere else.

### Gotchas

- **Seasonality is huge.** US fiscal-year-end (September) "use it or lose it" spike; India's March year-end rush. Need to seasonally adjust or everything looks like a signal.
- **Headline vs. real money.** US IDIQ ceilings and India AoN values are *potential* spend, not actual. They're heavily inflated, so conversion rates matter more than headline numbers.
- **Classified / black budget.** Some US spending just won't show up. Track the unclassified part and treat the gap as a known unknown.
- **India data is messy.** It's mostly PIB press releases, PDFs and exchange filings, not APIs. Expect a lot of scraping and LLM extraction ("pull rupee value, platform, service, vendor out of this press release").
- **Continuing resolutions (US)** delay new-start programs, which breaks lag assumptions in CR years. FY27 looks like a CR year.
- **Numbers don't always agree (India).** Different MoD/PIB releases give different AoN totals for the same year, so keep the source document next to every row.
- **Rules are changing (India).** A new Defence Acquisition Procedure (DAP-2026) is in draft or just finalised, so procurement timelines and categories may shift.

### MVP sketch

- Pick 4-5 signals per country that are easy to pull. US: DoD daily contract announcements, SAM.gov sources sought by NAICS, Daily Treasury Statement DoD line, FMS notifications, FRED ADEFNO/ADEFUO. India: PIB DAC/AoN releases, BSE order and "L1" filings, CGA monthly accounts, Standing Committee reports, service RFI pages.
- First concrete build: an **India AoN ledger**. Scrape every DAC release since ~2018 into rows, match each to later contract signings, and compute the conversion rate and lag. Nobody publishes this.
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

**Heads-up:** India has almost no APIs. It's PIB press releases, PDFs and exchange filings, so this is a scraping + LLM-extraction job. PIB can't be filtered by ministry via URL; use the MoD's own press-release page or the PIB archive.

Pipeline / pre-contract (leading)

| Source | Link | Access | Signal | Lead |
|---|---|---|---|---|
| DAC AoN approvals (via PIB) | [PIB all releases](https://pib.gov.in/Allrel.aspx?reg=3&lang=1), [MoD press releases](https://mod.gov.in/press-releases-ministry-defence), [PIB archive by ministry](https://archive.pib.gov.in/archive/phase2/archiveministry.aspx) | [PIB RSS](https://pib.gov.in/ViewRss.aspx?reg=3&lang=1) (not split by ministry); community scraper [PIB-Direct](https://github.com/jyotishman888/PIB-Direct) | ₹ value of approved proposals, ~6-10 meetings/yr. **No official dataset, so this is the thing to build** | Rules say ~74-106 weeks; really 2-5+ yrs |
| CCS approvals | via PIB / press | – | Final sign-off on big-ticket deals | weeks |
| MoD e-procurement | [defproc.gov.in latest tenders](https://defproc.gov.in/nicgep/app?page=FrontEndLatestActiveTenders&service=page) | scrape | Tender counts/values (mostly revenue + smaller capital) | 1-6 mo |
| Central Public Procurement Portal | [eprocure.gov.in/cppp](https://eprocure.gov.in/cppp/), [etenders.gov.in](https://etenders.gov.in/) | scrape | Same, for other central bodies | 1-6 mo |
| Service RFIs | [Army](https://indianarmy.nic.in/Tenderrfi/RFI), [Navy](https://indiannavy.gov.in/content/requests-information-rfi), [IAF](https://indianairforce.nic.in/rfp-rfi-eoi-and-cumulative-details-of-rfp/) | scrape | Earliest public sign of a requirement | 1-5 yrs |
| iDEX / DRDO TDF | [idex.gov.in](https://idex.gov.in/), [TDF](https://tdf.drdo.gov.in/) | – | Challenge topics = which tech is coming (small ₹) | 2-5 yrs |
| SRIJAN / Positive Indigenisation Lists | [srijandefence.gov.in](https://srijandefence.gov.in/) | PDFs | Import embargo dates force domestic orders (6th list Aug 2026: 405 items) | 1-3 yrs to embargo date |
| Make-I / Make-II | [makeinindiadefence.gov.in](https://makeinindiadefence.gov.in/) | – | Prototype approvals / EoIs | 2-4 yrs |
| DRDO tech transfers | [DRDO ToT](https://drdo.gov.in/drdo/en/offerings/transfer-of-technologies) | – | Tech handed to industry | 1-3 yrs |
| Standing Committee on Defence | [Sansad committee page](https://sansad.in/ls/committee/departmentally-related-standing-committees/7-defence), [PRS summaries](https://prsindia.org/parliamentary-committees/defence) | PDFs, annual (~March) | Service-wise projected vs allocated capex, committed liabilities | 0-12 mo |
| Parliament questions | [Lok Sabha Q&A](https://sansad.in/ls/questions/questions-and-answers), [Rajya Sabha Q&A](https://sansad.in/rs/questions/questions-and-answers) | faceted search | Contract/AoN counts, delays | explanatory |
| US arms-sale notices for India | [DSCA India tag](https://www.dsca.mil/Press-Media/Major-Arms-Sales/Tag/45781/india) (+ State Dept for 2026 on) | – | Proposed US sales to India | months |
| Procurement rules | [DAP-2020](https://ddpmod.gov.in/sites/default/files/2024-02/dap-2020-11-nov-21_0_0.pdf), [Draft DAP-2026](https://mod.gov.in/sites/default/files/DRAFT-DAP-2026_0.pdf), [DFPDS-2026](https://mod.gov.in/dod/sites/default/files/DFPDS-2026.pdf) | – | Regime changes. ⚠ not sure DAP-2026 is final yet | – |

Budget / cash (coincident)

| Source | Link | Notes |
|---|---|---|
| Union Budget | [indiabudget.gov.in](https://www.indiabudget.gov.in/), [Capital Outlay on Defence Services (Demand 21)](https://www.indiabudget.gov.in/doc/eb/sbe21.pdf), [PRS budget analysis](https://prsindia.org/) | Annual (Feb 1), BE vs RE |
| Controller General of Accounts | [Monthly dashboard](https://cga.nic.in/MonthDashboardReport/Published/list.aspx), [Monthly accounts review](https://cga.nic.in/Page/Monthly-Accounts-Review.aspx) | Monthly, ~1 mo lag. ⚠ press reports ministry-wise capex from CGA data, but need to confirm which statement has the defence line |
| GeM | [gem.gov.in/view_contracts](https://gem.gov.in/view_contracts) | MoD is GeM's biggest buyer; no bulk API |
| MoD Annual Report | [mod.gov.in annual reports](https://mod.gov.in/documents/annual-report), [FY26 report](https://mod.gov.in/sites/default/files/Annual-report-2025-26.pdf) | Contracts signed, programme status |
| CAG defence audits | [cag.gov.in defence](https://cag.gov.in/defence/new-delhi/en/audit-report), [data.gov.in](https://data.gov.in/catalog/cag-union-audit-reports) | Lags 2-3 yrs, good for cost overruns and delays |
| Dept of Defence Production | [ddpmod.gov.in](https://ddpmod.gov.in/en), [data.gov.in production & exports](https://data.gov.in/catalog/defence-production-and-export), [defenceexim.gov.in](https://defenceexim.gov.in/) | Annual production and exports |

Company / market

| Source | Link | Notes |
|---|---|---|
| BSE announcements | [bseindia.com announcements](https://www.bseindia.com/corporates/ann.html) | Unofficial JSON API behind the page; Python wrapper [BseIndiaApi](https://github.com/BennyThadikaran/BseIndiaApi). Filter for "order", "L1", "Letter of Intent" |
| NSE announcements | [nseindia.com filings](https://www.nseindia.com/companies-listing/corporate-filings-announcements) | Needs session cookies; wrapper [NseIndiaApi](https://github.com/BennyThadikaran/NseIndiaApi). ⚠ API path not confirmed |
| Nifty India Defence index | [niftyindices.com](https://www.niftyindices.com/indices/equity/thematic-indices/nifty-india-defence) | Market-implied, reacts same day to DAC news (equal-weight version launched Aug 2026) |
| Trade data | [TradeStat (Commerce)](https://tradestat.commerce.gov.in/eidb/commodity_wise_all_countries_import), [UN Comtrade](https://comtradeplus.un.org/) ([API](https://comtradedeveloper.un.org/)) | HS 93 arms; aircraft (88) and ships (89) sit elsewhere, and govt imports are patchy |
| SIPRI arms transfers | [armstransfers.sipri.org](https://armstransfers.sipri.org/) | Annual. India #2 importer 2021-25 (8.2% of global). Has order year, not just deliveries |
| Satellite imagery | [Copernicus Browser](https://browser.dataspace.copernicus.eu/) | Shipyards (Mazagon, GRSE, Cochin). Tracks deliveries more than contracts |

India context right now (from PIB releases):
- **FY26 was a record year:** 109 AoNs worth ₹6.81 lakh cr vs 503 contracts worth ₹2.28 lakh cr (~1:3). The capital budget was fully spent, and MoD credits the needs after Operation Sindoor ([PIB 2247977](https://pib.gov.in/PressReleasePage.aspx?PRID=2247977)). ⚠ Another report gives 55 AoNs / ₹6.73 lakh cr.
- **FY27 budget:** MoD ₹7.85 lakh cr (+15%), capital ₹2.19 lakh cr (~+22%) ([PIB 2222601](https://pib.gov.in/PressReleasePage.aspx?PRID=2222601)).
- **2026 DAC meetings:** 12 Feb ₹3.60 lakh cr; 27 Mar ₹2.38 lakh cr ([PIB 2246125](https://pib.gov.in/PressReleasePage.aspx?PRID=2246125)); 3 Jul ~₹52k cr; 7 Sep ~₹1.10 lakh cr.
- **FY26 production / exports:** ₹1.78 lakh cr ([PIB 2273824](https://pib.gov.in/PressReleasePage.aspx?PRID=2273824)) / ₹38,424 cr ([PIB 2248124](https://pib.gov.in/PressReleasePage.aspx?PRID=2248124)).
- **Post-Sindoor emergency procurement (EP-6):** reportedly capped around ₹40k cr, with contracts to close within 40 days. ⚠ Press reports only, not on PIB.
