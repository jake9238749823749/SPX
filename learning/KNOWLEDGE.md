# Knowledge base (read first every session)
Evidence levels: **P** proven here with data · **R** replicated elsewhere · **S** single source, unverified · **B** belief, no test yet.
Each entry: claim · level · source or test · date. Demote an entry if new evidence contradicts it.

## Trading and markets
- P: Retail intraday public signals on US500, XAUUSD and GBPUSD were worth 0-4 bp gross, and round-trip costs of 0.7-2.8 bp kill them. Source: 34 pre-registered tests, edge/SEARCH_LOG.md, 2026-10-15.
- P: Noise-area momentum decayed after publication on both US500 and gold. Source: edge/SEARCH_LOG.md.
- P: ORB on S&P micro futures: dev net +2.41 bp/trade, holdout net −2.26 bp/trade. Source: audits/001-orb-us500.md.
- R: ORB gross edge was negative in an independent 2015-26 replication (Krueger, MQL5, S). Source: sprawl lane 17.
- S: Overnight gold and S&P returns are concentrated in pre-2018 samples and shrink after spreads. Source: sprawl lane 15.
- B: Discretionary skill exists in fewer than 1-3% of retail traders. Source: Barber-Odean-style studies cited by sprawl lanes; not re-verified.

## Method
- P: Gross-to-cost ratio determines viability. Per-trade move divided by round-trip cost is the first filter.
- P: Pre-registration plus blind replication caught no false positives in this program. Its value is ruling things out fast.
- P: Holdout data is spent after one use. A "post-hoc exception" must be logged before running.
- B: A 120-day forecast verdict is underpowered for small Brier skill; roughly 400 days are needed. Source: system/ANALYSIS_2026-10-15.md (approximate, not computed).

## AI and research
- P: AI made research fast in this repo: 34 tests and 20 lanes in one day.
- S: LLM trading results post-cutoff are mostly within noise of buy-and-hold (StockBench, Alpha Arena secondhand). Source: learning session 2026-10-15.
- B: LLMs memorise pre-cutoff prices, so backtests of LLM judgment are contaminated.

## Open questions (answer these with evidence, not opinion)
1. Is there any retail-accessible venue where a limit-order trader earns the spread? (test with a small real-money fill log)
2. Does a volatility regime measure (ATR percentile, VIX) change the sign of any cost-adjusted rule in 2023+ data?
3. How much of the S&P's daily range is known before 10:00? (could a forecaster use it)
