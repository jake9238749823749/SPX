# Research sprawl: 20 Haiku agents hunting for a surviving edge

## SHARED BRIEF (prepend to every agent)
You are one of 20 scouts working for a falsifier. Your job is to find evidence. Building a strategy is not your job, and neither is liking one. The program has already killed 32 tests, all using real bid/ask data:
- intraday rules on US500, gold and GBPUSD;
- daily and multi-week trend;
- noise-area momentum. It decayed after publication: ES Sharpe 1.78 before publication, -0.19 after.
- the FTMO challenge priced as an option.

**The law.** Net = gross − cost. Public intraday effects run 0-4 bp gross and decay after publication. Retail round-trip cost: US500 CFD about 1.0-1.4 bp, MES about 0.7 bp, gold CFD about 2.8 bp, MGC about 0.65 bp plus CME fees, GBPUSD about 1.1 bp. Futures embed financing, so there is no free carry.

**Hard constraints.** Instruments: US500, XAUUSD, GBPUSD or their CME futures. At least 4 trades a week. Must be legal under FTMO's rules: no HFT or latency arbitrage, no grid or martingale, no cross-account hedging, and no "one-sided bets", "overleveraging" or "inconsistent sizing". FTMO Futures closes all positions at 16:10 ET.

**What qualifies.** Evidence from 2023 onward of gross ≥ 2× round-trip cost on a retail-accessible venue. Preferably out-of-sample, forward-tested, or independently replicated.

**Output.** At most 250 words:
1. Verdict line: FOUND / NOTHING.
2. Up to 3 candidates, each with: exact rules and parameters (quoted from source), URL, date, sample period, gross per trade in bp if computable, cost assumption, whether out-of-sample or replicated, and the evidence that might disconfirm it.
3. The closest miss, always.

**Rules.** Never invent numbers. Mark anything inferred as INFERRED. Vendors, "verified" myfxbook/MQL5 signals and backtests without costs are evidence of nothing unless you can extract a rule and its sample. Before returning, look for the strongest reason each find is false.

## THE 20 ASSIGNMENTS

**Academic and quant frontier (2023+)**
1. SSRN and arXiv q-fin, 2023-2026: intraday S&P/ES predictability that survives costs. Search: "intraday momentum after publication", "ES microstructure 0DTE", "end-of-day order imbalance", "market-on-close imbalance S&P".
2. The 0DTE options footprint on SPX intraday. Dealer gamma and hedging flows, published since 2023. Any measurable intraday drift or reversal timed to known flows: 0DTE expiry hour, 15:50 MOC, 14:00 FOMC. GEX already failed its gate, so look for something different.
3. Index event mechanics: S&P rebalances, quad witching, month-end and quarter-end pension rebalancing, the turn of the month. Need effect size in bp, sample from 2023 on, and how often it occurs. Will it reach 4 a week if combined?
4. Gold-specific flows: LBMA auction imbalances, Shanghai Gold Exchange premium and the Asian session, COMEX delivery cycles, central-bank buying days, gold-ETF (GLD) creation and redemption. Any intraday or overnight timing effect after 2023.
5. GBPUSD: the WMR 4pm fix after the 2015 rule changes, BoE event drift, and the London-NY overlap. 2023+ evidence only.
6. Macro announcements: CPI, NFP and FOMC pre-announcement drift (Lucca-Moench) and its post-2015 status. Post-announcement drift in ES/MES at the minute level. Has the pre-FOMC drift come back?

**Practitioner cracks**
7. Elite Trader, Futures.io (formerly BMT), and r/algotrading posts with backtests including costs. Mine for rules that report MES/ES or MGC results after 2023 with commissions, then find their replications or debunkings.
8. Quantpedia, Alpha Architect, QuantConnect forums, Robot Wealth, Quantocracy, 2023-2026: which intraday or short-horizon strategies have *recent* out-of-sample updates, not just original backtests?
9. Github code search: repos with pre-registered or walk-forward results on ES/MES/SPY intraday, with cost models. Read the README and results files. Rank by evidence quality, not stars.
10. TradingView open-source strategies with the most likes on SPX/ES/XAUUSD (ORB, VWAP, RSI-2, Bollinger fade). Extract exact default parameters. Flag any with commissions and slippage set above zero.
11. Prop-firm forums and Discords (FTMO, Topstep, Apex, Tradeify) and payout-proof threads. What do traders who get paid repeatedly actually do? Separate survivorship stories from rules you could test.
12. MQL5 CodeBase: the most-downloaded *open-source* EAs for XAUUSD and US500. Reject grids, martingales and averaging-down. Quote entry and exit logic.

**Structural and market-design angles**
13. FTMO Futures fine print and every competitor's: payout terms, scaling, consistency rules, and fee structures. Is there any firm whose rule set gives a zero-edge trader positive EV? Our model for FTMO was negative. Compute it for the others.
14. Cost-reduction cracks: commission tiers, CME micro fee schedules, and broker rebates on micros. Can anyone legitimately reach MES or MGC below 0.5 bp all-in?
15. Overnight vs intraday return decomposition for ES and gold after 2023 (the "overnight drift" literature). Is any decomposition tradeable within FTMO's 16:10 ET close?
16. Volatility-regime conditioning: any published 2023+ study showing that intraday edges hold only on high-VIX or high-ATR days, enough to clear 2× cost on those days.

**Disconfirmation squad**
17. Find every published replication failure from 2023 on for: ORB, VWAP reversion, RSI-2, noise-area/intraday momentum, turn of the month and pre-FOMC drift. Give effect size before and after.
18. Find evidence that retail futures fills on MES/MGC run worse than the quoted spread (slippage studies, broker 605/606 data, Topstep execution complaints with numbers).
19. Survivorship audit: myfxbook/MQL5 "top" signals for gold and US500 that were live in 2023 and are now dead. Report the death rate and the typical failure shape (grid blow-up, drawdown, abandonment).
20. Red team: argue with sources that *no* retail intraday edge on these instruments survives 2023+ costs. Then name the single strongest counterexample you found. If it's real, it overrides your own verdict.

## WHAT I DO WITH YOUR OUTPUT
I merge all 20 reports, deduplicate them, and rank by evidence quality: a replicated out-of-sample result beats a forward test, which beats a cost-inclusive backtest, which beats a claim. Every candidate that clears the 2× cost bar on paper gets a pre-registration and one DEV run on our 2021-24 data: S&P from HistData, gold from HistData, both bid/ask. The 2025-26 holdout opens only after a DEV pass, and only once. A candidate that can't be written as exact rules is dropped. If all 20 return NOTHING, the program's conclusion stands: no systematic edge at this cost tier.

Cost cap for this sprawl: 20 agents × about 30k tokens. No agent re-searches another's lane. A thin result is a valid result: "NOTHING plus the closest miss" is worth more than a stretched FOUND.
