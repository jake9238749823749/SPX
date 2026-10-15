# Knowledge base (read first every session)
Evidence levels: **P** proven here with data · **R** replicated elsewhere · **S** single source, unverified · **B** belief, no test yet.
Each entry: claim · level · source or test · date. Demote an entry if new evidence contradicts it.

## Trading and markets
- P: Retail intraday public signals on US500, XAUUSD and GBPUSD were worth 0-4 bp gross, and round-trip costs of 0.7-2.8 bp kill them. Source: 34 pre-registered tests, edge/SEARCH_LOG.md, 2026-10-15.
- P: Noise-area momentum decayed after publication on both US500 and gold. Source: edge/SEARCH_LOG.md.
- P: ORB on S&P micro futures: dev net +2.41 bp/trade, holdout net −2.26 bp/trade. Source: audits/001-orb-us500.md.
- S: Independent 2015-26 replication of the Zarattini ORB on SPX CFD (Krueger, MQL5, self-published): gross +0.119R (t 2.4), net −0.081R after the author's costs. Source: sprawl lane 17, audits/001-orb-us500.md §9.
- S: Overnight gold and S&P returns are concentrated in pre-2018 samples and shrink after spreads. Source: sprawl lane 15.
- B: Discretionary skill exists in fewer than 1-3% of retail traders. Source: Barber-Odean-style studies cited by sprawl lanes; not re-verified.

## Method
- P: Gross-to-cost ratio determines viability. (The gold DEV used a flat MGC cost of 0.65 bp; at 2021-22 gold prices of about $1,900 the real MGC round trip was about 1.5 bp. The gold verdict still holds because gross was negative. Source: sprawl lane 14, edge/SEARCH_LOG.md.) Per-trade move divided by round-trip cost is the first filter.
- P: Pre-registration plus holdout caught two false positives: U-NA (noise-area, US500) and ORB both passed DEV and failed holdout. Source: edge/SEARCH_LOG.md, audits/001-orb-us500.md. This is the evidence the protocol is worth keeping.
- P: Holdout data is spent after one use. A "post-hoc exception" must be logged before running.
- B: A 120-day forecast verdict is underpowered for small Brier skill; roughly 400 days are needed. Source: system/ANALYSIS_2026-10-15.md (approximate, not computed).

- S: "Forecast-to-Fill" gold trend (arXiv 2511.08571) headline Sharpe 2.88 is self-reported and unreplicable from the text; its 2x-cost row is −1.00, frequency is 2.3/wk, and capacity arithmetic doesn't reconcile. Source: audits/002-forecast-to-fill.md.

## AI and research
- P: AI made research fast in this repo: 34 tests and 20 lanes in one day.
- S: LLM trading results post-cutoff are mostly within noise of buy-and-hold (StockBench, Alpha Arena secondhand). Source: learning session 2026-10-15.
- B: LLMs memorise pre-cutoff prices, so backtests of LLM judgment are contaminated.

## Open questions (answer these with evidence, not opinion)
- Q1 status: P (paper answer, learning/MICROSTRUCTURE_Q1.md). Tick math shows no retail edge at MES/MGC fees; not yet tested with queue data.
1. Is there any retail-accessible venue where a limit-order trader earns the spread? (test with a small real-money fill log)
2. Does a volatility regime measure (ATR percentile, VIX) change the sign of any cost-adjusted rule in 2023+ data?
3. How much of the S&P's daily range is known before 10:00? (could a forecaster use it)
