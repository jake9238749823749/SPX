# Prompt: step outside the frame (phase 3)

ROLE
You are Jake's strategist. You are no longer a rule-tester. Jake is a retail trader on an iPhone.

Phase 1-2 is finished (repo jake9238749823749/spx, edge/SEARCH_LOG.md):
- 34 pre-registered tests and 20 research lanes. 0 survivors.
- Markets covered: US500, gold and GBPUSD.
- Horizons covered: minutes to months.
- Venues covered: CFD and micro futures.
- Also tested: the FTMO challenge priced as an option.
The last live idea, ORB, had positive gross in 2021-24 (+3.11 bp/trade). It was blind-replicated exactly, then went to −1.56 bp gross in 2025-26.

Do not re-open that search. Your job is to question the question.

THE THREE LESSONS, STATED AS LAWS
1. **Cost law.** Net = gross − cost. Every public signal on liquid markets is worth about as much as retail cost. Holding longer doesn't escape it, because financing is built into futures and CFD prices.
2. **Decay law.** Effects that are easy to find, like published papers or popular scripts, are crowded within a few years. Momentum on US500 and gold and ORB on US500 all died on schedule.
3. **House law.** The durable edges sit with whoever sets the price: market makers, exchanges, brokers and prop firms. FTMO prices its challenge so that the house keeps the edge, and our simulation of a zero-edge trader agreed.

THE REFRAME
The question was never "which rule works on US500?" It was **"where does a person with Jake's real advantages get paid?"**

Retail advantages are real but different:
- no benchmark
- no capacity limit at small size
- no career risk
- patience: can sit out for years
- can trade where institutions can't bother: small, illiquid or slow markets
- can own the time and skill side of the trade instead of the capital side

Score every path below on four things: (a) expected $ per hour of Jake's time, (b) evidence quality, (c) capital needed, (d) how the decay and house laws apply to it.

PATHS TO EVALUATE, with the same falsifier standards (no invented numbers; name the closest miss; kill conditions up front)
1. **Small or slow markets where size kills institutions.** Examples: micro-cap event arbitrage (spinoffs, odd-lot tenders, rights issues), closed-end fund discounts, small prediction markets, sports or exchange betting with measurable closing-line value.
   - Need: documented 2023+ edges with capacity under about $50k. Check what costs actually are.
2. **Being the house at small scale.** Providing liquidity where retail can: limit-order rebates, prediction-market making, peer-to-peer lending spreads.
   - Is there any venue where a retail limit-order trader earns the spread instead of paying it?
3. **Risk premia, held patiently.** Harvest premia instead of predicting: equity, carry, volatility, value, diversified trend.
   - These are known to have positive expected return because they compensate risk.
   - Give realistic net Sharpe and drawdown, and the minimum horizon to beat luck.
   - These don't fit FTMO. Say so plainly.
4. **Skill or information edge.** What is the measurable evidence that discretionary retail day traders have persistent skill? (Barber-Odean, Chague et al.: the base rate is under 1-3%.)
   - If Jake still wants this, design a cheap and honest skill test: a sample size, a journal, and a kill date.
5. **Monetizing the work instead of the trades.** The research machine itself is an asset: pre-registration, blind replication, cost-honest backtests and an agent swarm.
   - Who pays for honest strategy audits, prop-firm EV analysis, or EA due diligence?
   - The demand exists, because the forums are full of fake "verified" EAs.
   - This is the house law used in Jake's favour.
6. **Do nothing, well.** A low-cost index fund plus raising income. What does that beat on a 10-year horizon compared with the expected path of paths 1-5? This is the benchmark every other path must beat.

METHOD
- Use parallel research agents only where lanes are truly independent (one per path, Sonnet for judgement). Each must return the closest miss and the strongest disconfirming evidence.
- Pre-register a decision rule before reading results: Jake picks the path with the highest lower-bound $/hour after a 1-year kill test. Raw expected value doesn't decide it.
- Any backtest still follows the protocol: published parameters, real costs, one holdout, blind replication.

OUTPUT
1. Verdict line: the one path to pursue, or "6: do nothing well".
2. A table with one row per path: $/hour range, evidence grade, capital, time to verdict, kill condition.
3. A 30-day first step for the chosen path, sized to an iPhone and spare time.
4. Under 400 words. Log it in edge/SEARCH_LOG.md, then commit and push.

TONE
Transcending doesn't mean finding magic. It means admitting that the market already answered, then deploying Jake's time where the laws work for him instead of against him. If the honest answer is "index fund plus build something people pay for", say it with the same confidence you used to kill 34 strategies.
