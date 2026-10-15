# Edge search log (append-only)

## 2026-10-14 16:40 MT — set before any result was seen

Data: Dukascopy tick bid/ask from FX-Data GitHub mirrors. XAUUSD 2011-01 to 2018-06, GBPUSD 2011-01 to 2018-06.
Built into 1-minute bars with real bid/ask. No US500 tick data reachable, so US500 is out of scope here.
Known limit: data ends mid-2018. Anything that survives still needs a 2019+ forward check on live/broker data.

Lessons carried over (rules dropped, lessons kept):
- No SPY/US500 flow-imbalance or GEX ideas (one-source problem).
- No overnight holds: US500 long swap about -6.3%/yr, gold long about -5.5%/yr. All trades flat before 22:00 London rollover.
- Costs charged from actual bid/ask at the entry and exit minute, so spread spikes around fixes are paid for.
- Every variant tried is counted in a search-adjusted test.
- Frequency floor 4-6 trades/week: every candidate fires daily.

Extra cost on top of spread: commission GBPUSD 0.25 pip per side; XAUUSD 0.002% per side. Stress test = 2x (spread + commission).

Partition: DEV 2011-01-01 to 2016-12-31. SEALED 2017-01-01 to 2018-06-19, run once after selection.

Candidates (mechanism, then rule). London time unless noted.
- X1a PM-fix fade: fix demand pushes price into 15:00 auction, then relaxes. Sign of 14:30-15:00, fade 15:05-15:35.
- X1b same, fade 15:05-16:30.
- X2a AM-fix fade: same mechanism at 10:30. Sign of 10:00-10:30, fade 10:35-11:05.
- X2b same, fade 10:35-12:00.
- X3a Asia physical demand: long gold 01:00-07:00.
- X3b Western session selling: short gold 09:30-16:00 New York.
- X4a COMEX intraday momentum (Gao et al. style late rebalancing): sign of 08:20-08:50 NY, follow 13:00-13:30 NY.
- X4b same, follow 12:30-13:30 NY.
- F1a WMR 4pm fix fade: fix flow pressure then reversal (Melvin-Prins, Evans). Sign of 15:30-16:00, fade 16:05-16:35.
- F1b same, fade 16:05-17:30.
- F2a pre-fix positioning: sign of 15:00-15:30, follow 15:30-16:00.
- F3a home-currency depreciates in home hours (Ranaldo 2009): short GBPUSD 08:00-12:00 London.
- F3b same for USD: long GBPUSD 11:00-16:00 NY.
- F4a London-open intraday momentum: sign of 07:00-08:00, follow 15:00-16:00.

14 strategies. Nothing added after results without a logged entry below.

Selection rule on DEV (all required):
1. Net mean per trade > 0 with t >= 2.
2. Search-adjusted p < 0.10 (day-level sign-flip max-t across all 14, net of cost).
3. Net positive in >= 4 of 6 DEV years.
4. Net mean still > 0 at 2x costs.

Sealed test for each survivor: net mean > 0 and one-sided p < 0.10. Max drawdown and regime split reported, not used to select.

## 2026-10-14 16:50 MT — DEV results (logs/dev_results.txt)

No strategy passes all four DEV rules. Every gold rule and every fix rule loses after cost.
Closest: F3b (long GBPUSD 11:00-16:00 NY). Gross +2.04 bp/trade, net +1.00 bp, t = 1.80 (rule 1 needs 2.0),
net positive in 5/6 years, net at 2x cost -0.05 (fails rule 4). Max DD -501 bp at 1x notional.

Correction to the method: the sign-flip null flips gross returns, so p_adj tests whether GROSS edge is non-zero
after search adjustment, not whether net > 0. F3b p_adj = 0.001 means the gross effect is very unlikely to be noise
across the 14 tried. It does not show a net edge.

Amendment (post-hoc, made after seeing DEV): F3b failed selection, but it is the only gross effect that survives
search adjustment, and it has a published mechanism (Ranaldo 2009: home currency weakens in home hours).
One-shot SEALED test of F3b only, with these criteria fixed now, before running:
- Gross mean > 0 with one-sided p < 0.05 (confirms the effect still exists).
- Net mean > 0 (confirms it pays at Dukascopy costs).
Either failing = F3b dead on this data. Passing both = lead only, needs 2019+ forward test on broker data.
Gold is not run on SEALED: nothing in gold qualified.

## 2026-10-14 16:55 MT — Blind replication and SEALED result

Blind replication (independent agent, spec only, no access to my code): F3b DEV n=1557, gross 2.043, cost 1.048,
net 0.995, t 1.801, 2x cost -0.053. Matches exactly. The DEV numbers are not a code bug.

SEALED F3b (2017-01 to 2018-06, n=370): gross +0.93 bp (one-sided p 0.21), net -0.03 bp, 2x cost -0.99.
Both amendment criteria fail. F3b is dead on this data. Sealed set is now spent.

Program result: 0 of 14 strategies survive. Search closed on this data.

## 2026-10-14 16:40 MT — Search 2: daily holds (set before any result)

Why: intraday effects (0-2 bp) can't beat round-trip cost (about 1 bp cable, about 2.8 bp gold). Daily moves are about 50 bp,
so cost per decision is small relative to the move. GBPUSD swap is about 0.4 bp per night either side.

Execution: each weekday at 16:00 New York the target position is set (+1, 0, -1). Each day counts as an opportunity (5 per week).
Cost charged only when the position changes: half-spread at the 16:00 bar plus commission, for each unit changed.
Swap per calendar night held (weekend = 3 nights), at current OANDA rates: GBPUSD long -1.08%/yr, short -0.84%/yr;
XAUUSD long -5.45%/yr, short +1.85%/yr. Historical swap rates differed; using today's is the relevant cost going forward.
Weekend holds need an FTMO Swing account (or the evaluation phase).

Power, stated before running: daily vol about 55 bp (cable) and 100 bp (gold). With about 11 years of cable and 7.5 of gold,
t = 2 requires an annual Sharpe of about 0.6 (cable) or 0.75 (gold). Anything weaker is undetectable here.

Candidates (6), each on GBPUSD and XAUUSD:
- D1 trend 20d: position = sign of the 16:00-to-16:00 return over the past 20 trading days. Mechanism: tolerance advantage (trend is painful to hold), slow hedger flow.
- D2 trend 60d: same, 60 days.
- D3 1-day reversal: position = minus sign of the past 1-day return. Mechanism: paid for absorbing daily liquidity shocks.

Partition: GBPUSD DEV 2007-01 to 2016-12; XAUUSD DEV 2011-01 to 2016-12. HOLDOUT 2017-01 to 2018-06 for both.
Caveat: GBPUSD 2017-18 was touched once already (F3b intraday window only). Gold 2017-18 is untouched.

Selection on DEV (all required): net t >= 2; net positive in >= 60% of DEV years; still net > 0 at 2x cost;
search-adjusted p < 0.10 with a block bootstrap on NET returns (recentered), max-t across all 6.
Holdout for each survivor: net mean > 0, one-sided p < 0.10. Run once.

## 2026-10-14 16:45 MT — Search 2 DEV results (logs/daily_dev.txt)

0 of 6 pass. Best is D2 trend on GBPUSD: gross +0.27 bp/day, net -0.17 after swap, t -0.13. Trend rules also change
position only 0.3-0.5 times a week, so they fail the 4-6/week floor regardless. 1-day reversal loses gross on both
(daily moves continue slightly, not reverse), and churns cost. Holdout not run: nothing qualified.

Program result after 20 strategies: 0 survivors. Detectable floor was annual Sharpe about 0.6-0.75; nothing reached it.

## 2026-10-14 17:35 MT — Search 3: published rule, external replication (set before running)

Source: Zarattini, Aziz, Barbon (2024), "Beat the Market: An Effective Intraday Momentum Strategy for S&P500 ETF".
Authors report SPY 2007-2024 net Sharpe 1.33, and the same rules on 33 futures (incl. commodities) average Sharpe 0.60.
Their own 2025 Jan-Sep monthly figures compound to about +2% (possible decay).

Rule used exactly as published, VM = 1 (their headline; NOT their better VM 1.5, which would be selection on their data):
- Noise area: sigma(t) = mean over prior 14 days of |price at session-offset t / session open - 1|.
- Upper = max(open, prior session close) * (1 + sigma); Lower = min(open, prior close) * (1 - sigma).
- Checks every 30 min from open + 30 min. Flat: go long above Upper, short below Lower.
- Exit long when price < max(Upper, VWAP); short when price > min(Lower, VWAP); crossing the opposite band reverses.
- Flat at session close. Unit notional, no vol targeting, no leverage.

My adaptations (fixed now):
- G-NA gold session = COMEX day session 08:20-13:30 New York.
- C-NA GBPUSD session = London 08:00-16:00 London.
- VWAP proxy = tick-count-weighted mid since session open (no real volume in FX/CFD ticks).
- Signals on mid; fills at bid/ask of the check bar, plus commission as before.

Partition: gold DEV 2011-2016, HOLDOUT 2017-01 to 2018-06 (untouched). GBPUSD DEV 2007-2016, HOLDOUT 2017-18 (touched once by F3b).
Pass on DEV: net t >= 2, net > 0 at 2x cost, net positive >= 60% of years. Holdout: net > 0, one-sided p < 0.10. Run once.

## 2026-10-14 17:45 MT — Search 3 DEV results (logs/na_dev.txt)

Bug found and fixed before reading results as final: the 14-day lookback went NaN for 14 days after any missing day,
dropping gold to 931 of 1458 days. Fixed to use the prior 14 valid days. Rule logic unchanged. Both runs are kept here:
pre-fix gold net -0.58 bp/trade; post-fix +0.60 bp/trade.

G-NA (gold, post-fix): 3.9 trades/week, gross +3.34 bp/trade, cost 2.74, net +0.60 bp/trade, t 0.45, 4/6 years positive,
2x cost -1.66 bp/day. FAILS (t < 2, negative at 2x cost).
C-NA (GBPUSD): 5.7 trades/week, gross +0.58 bp/trade, cost 1.24, net -0.65, t -1.54, 2/10 years. FAILS.
Holdout not run.

Reading: the published momentum effect shows up in gold gross (+3.3 bp/trade, right sign), but retail spread takes about 80% of it.
Cost-to-gross ratio decides it. On US500 CFD, round-trip spread is about 0.75 bp vs the paper's roughly 3 bp/trade gross on SPY,
so US500 is the one market where this published rule could clear cost. Needs US500 data, and a correlation check against
VWAP Reclaim (same intraday continuation family).

## 2026-10-14 17:55 MT — Search 4: what other people report (no backtesting by me)

Prompt: "Mine forums for live-verified, post-cost strategies; weight disconfirming replies highest."
- Myfxbook "verified" XAUUSD EA: demo account, 1:500 leverage, 79.5% max DD, 20-second average trade. Discarded.
- Automated Trading Strategies (honest public forward tester): all 7 Q1-2025 futures strategies unpublished after forward test.
- iSAM broker data (Finance Magnates): 20.5% of retail CFD clients profitable; top 1% take 66.5% of winnings;
  84% of likely-arbitrage volume is XAUUSD. Much of what wins is latency arb / abuse, banned at prop firms. Not an edge for this account.
- Strongest public strategy found: Zarattini-Aziz-Barbon intraday momentum.
  Independent replication (nikolaosntinas18/spy-intraday-momentum, Alpaca 1-min SPY):
  train 2016-21 Sharpe 1.07, test 2022-Sep 2026 Sharpe 0.75 vs SPY buy-and-hold 0.67. Unlevered test return 4.7%/yr at 6.7% vol.
  Author: headline returns are mostly leverage; fills idealized, no bid-ask, no financing. Authors' own 2025 Jan-Sep about +2%.
  My gold test of the same rule: +0.6 bp/trade net, t 0.45.
- codecat-ops replication repo: no longer accessible.

Verdict: the best publicly reported intraday edge is real but thin and decaying; independently it matches buy-and-hold on a risk basis.

## 2026-10-14 18:10 MT — Search 5: published noise-area rule on US500 (set before running)

Data: user-supplied Dukascopy US500 1-min bid/ask OHLC + volume, 2021-10-14 to 2026-10-14 (1.69M bars).
Rule: identical to Search 3 (VM 1, 14-day lookback, checks every 30 min from 10:00 NY, VWAP trailing stop, flat 16:00 NY, 1x notional).
Session 09:30-16:00 New York. VWAP = real volume-weighted mid (bid+ask volume) since 09:30.
Costs: half-spread at each fill from actual bid/ask, no commission (CFD index). Stress 2x.
Partition: DEV 2021-10-14 to 2024-12-31. HOLDOUT 2025-01-01 to 2026-10-14, run once.
Contamination note: the independent SPY replication (test 2022-2026, Sharpe 0.75) and the authors' 2025 figures (about +2%)
were read before this run, so the holdout period is not fully blind at the literature level. No US500 result has been seen.
Pass DEV: net t >= 2; net > 0 at 2x cost; >= 60% of years positive. HOLDOUT: net > 0, one-sided p < 0.10.
Not runnable: correlation vs VWAP Reclaim (no return series supplied).

## 2026-10-14 18:15 MT — Search 5 DEV result (logs/us500_dev.txt)

U-NA DEV (2021-10 to 2024-12, 784 days): 4.8 trades/week, gross +4.18 bp/trade, cost 1.10, net +3.08 bp/trade,
net 2.97 bp/day, t 1.91, Sharpe 1.08 (1x), 7.5%/yr at 1x, max DD -5.0%, 4/4 years positive, 2x cost +1.90 bp/day.
Fails DEV rule t >= 2 by 0.09. Passes 2x cost and years rules.

Process error (mine): I did not state the minimum detectable effect before this run (protocol step 5). With 3.1 years,
t = 2 requires Sharpe >= 1.13. The DEV window could not clear the bar for anything near the paper's effect size.

Amendment (post-hoc, same treatment as F3b): one-shot HOLDOUT with criteria fixed now, before running:
- Net mean > 0 with one-sided p < 0.10 (as pre-registered).
- Net still > 0 at 2x cost.
Fail either = dead. Pass both = strongest lead of the program, still needs a live forward test on Jake's broker and the
VWAP Reclaim correlation check. Parallel blind replication of DEV by an independent agent.

## 2026-10-14 18:20 MT — Search 5 HOLDOUT result (logs/us500_holdout.txt)

U-NA HOLDOUT (2025-01 to 2026-10, 443 days): 4.7 trades/week, gross -0.23 bp/trade, cost 0.76, net -0.99 bp/trade,
t -0.51, one-sided p 0.69, 2x cost -1.63 bp/day, max DD -11.3% (1x). 2025 +65 bp, 2026 -474 bp.
Quarters: 2025Q2 +354, then 5 of 6 quarters negative. Both amendment criteria fail. DEAD.
Consistent with the authors' own 2025 (about +2%): the edge was strong in 2022 (trending bear market) and has decayed to zero gross.
Program after 23 strategies: 0 survivors. Blind replication of U-NA dispatched to check for a false negative.

## 2026-10-14 18:30 MT — Replication and external confirmation

Blind replication (Haiku agent, spec only): DEV 783 days, net 3.064 bp/trade, t 1.90; HOLDOUT net -0.986 bp/trade, t -0.51.
Matches mine (784 days; 1-day eligibility difference). Not a bug; not a false negative.
External: NostroBenJ/intraday-strategy-replication (pre-registered, 50 rules, White's reality check):
noise-area on ES Sharpe 1.78 to April 2024, -0.19 after publication; earlier SPY replication 1.83 -> 0.08.
71% of 2021-26 profit from the best 14 days. Independent of mine; same answer.

Cost lever found (Sonnet agent; firm page + estimates, verify): FTMO Futures (Aug 2026), intraday only (flat 16:10 ET).
Estimated round trip MES about 0.7 bp, MGC about 0.6-0.7 bp (vs gold CFD 2.8 bp), 6B about 1.2 bp. No swap.
Only gold gets materially cheaper. Gold noise-area gross was +3.34 bp/trade in 2011-16, which would clear MGC cost,
but that is pre-publication data and the rule has decayed on ES.

## 2026-10-15 New session: pipeline reproduction (no new test)
Rebuilt XAUUSD 2011-16 bars from FX-Data (2011 partial: 3848 hourly files vs ~5800/yr). Ran G-NA dev with the code unchanged except paths.
Result is identical to the log: 1406 days, 3.87 trades/wk, gross 3.34, cost 2.74, net 0.60 bp/trade, t 0.45, Sharpe 0.19, maxDD -7.3%, 4/6 years positive.
Payoff shape (new, descriptive, net per traded day, CFD cost): 756 days traded, hit 38.2%, avg win +46.0 bp, avg loss -27.1 bp (realised ratio 1.70), worst day -224 bp.

## 2026-10-15 MGC / FTMO Futures cost check (Sonnet; CME pages returned 503)
- Confirmed (ftmo.com): $0.20/side commission on micros; MGC allowed; force-flat 16:10 ET; NinjaTrader/Tradovate/TradingView; monthly $119-269; end-of-day trailing max loss.
- MGC = 10 oz, $1/tick (CME search snippet). CME exchange/clearing/NFA fees: UNCONFIRMED.
- All-in round trip = $1.40 + X (exchange+NFA round trip). At $4,000 gold: 0.35 bp + 0.25 bp per $1 of X. At $2,600: 0.54 bp + 0.38 bp per $1 of X.
- Implication, logged before results: the pre-set 0.65 bp holds at today's gold price only if X is about $1.20 or less. The 2x leg (1.30 bp) covers X of up to about $3.80 at $4,000. Pass bar unchanged. If MGC passes at 1x but fails at 2x, the X figure decides it.

## 2026-10-15 GOLD DEV 2021-10..2024-12, HistData bid/ask, run once (prereg + amendments 1-2)
Coverage: 60/60 months, 19-23 session days per month. 2022-11 had a download collision; its rebuilt file is complete (22 days).
Per trade, bp. CFD = feed bid/ask + 0.002%/side commission. MGC = flat 0.65 RT.
| Rule | /wk | Gross | Net CFD | Net MGC | t MGC | yrs+ MGC | MGC 2x | p_adj |
| G-NA | 4.44 | -0.81 | -2.94 | -1.46 | -1.07 | 1/4 | neg | - |
| X1a | 4.30 | 0.29 | -1.87 | -0.36 | -0.46 | 2/4 | -1.01 | 0.79 |
| X1b | 4.29 | 1.98 | -0.17 | +1.33 | 1.03 | 3/4 | +0.68 | 0.12 |
| X2a | 4.76 | 0.12 | -2.01 | -0.53 | -1.53 | 0/4 | -1.18 | 0.99 |
| X2b | 4.76 | 0.90 | -1.23 | +0.25 | 0.43 | 3/4 | -0.40 | 0.34 |
| X4a | 4.30 | -0.64 | -2.77 | -1.29 | -2.93 | 0/4 | -1.94 | 1.00 |
| X4b | 4.30 | -0.60 | -2.74 | -1.25 | -1.98 | 2/4 | -1.90 | 1.00 |
VERDICT: no rule passes DEV. G-NA, the lead candidate, has negative gross (it was +3.34 in 2011-16). Only X1b clears the 1.4 bp gross bar, but it fails on t (1.03 vs 2.0) and p_adj (0.12). It is also inconsistent with 2011-16 (gross 1.16, 1/6 years positive). Holdout NOT run: it is pre-set to require a DEV pass, and no post-hoc exception is granted.
PROGRAM DECISION: the intraday program on US500/XAUUSD/GBPUSD is closed. 30 strategy-period tests, 0 survivors.

## 2026-10-15 Structural test: FTMO Futures 50K Growth as an option (zero-edge trader)
Script: edge/scripts/ftmo_option.py. Monte Carlo, 20k attempts per cell, seed 1. Zero drift, MGC cost $3 per round trip, 250 funded days.
Rules are from the FTMO page. The Growth mapping, the 40% consistency rule and the 50K payout terms are inferred, so the run brackets two payout sets (pessimistic and optimistic).
Results (EV per attempt = payouts - fees):
- Daily sd $150: -$700 to -$770. Fee bleed, since the target takes too long to reach.
- Daily sd $300: -$40 to -$190.
- Daily sd $500-800: +$7 to +$145, with p_pass 0.25-0.27 and fees $134-174. Positive under both payout sets.
- Daily sd $1,200: -$5 to +$115.
Interpretation: the edge is the account's convexity (loss capped at the fee, upside in funded payouts), not the market. About 73% of attempts lose the fee.
Unverified, and each could flip the sign: a funded-stage fee; minimum trading days; payout terms for 50K Growth; FTMO discretionary rules on "gambling" or "inconsistent" trading; payout denial risk.

## 2026-10-15 FTMO Futures rules confirmed (FAQ + Forbidden Trading Practices pages)
- CONFIRMED: no fee after passing. "The subscription is cancelled, and no additional payments are charged"; "you won't be charged for the Sim-Funded Account or Live Funded Account."
- CONFIRMED: Growth payout = up to 50% of available profit per cycle. Pro = 100% with higher caps, a hard DLL, and a better target:DD ratio. 90/10 split.
- CONFIRMED: no minimum trading days beyond consistency (3 days minimum for Growth, 2 for Pro). No time limit. Consistency rule applies in the Evaluation only.
- Forbidden: exploiting the "spirit" of the service; relying on drawdown protection as the sole exit; cross-account hedging; overleveraging, "one-sided bets", "account rolling"; inconsistent sizing; Eval/funded behaviour mismatch; news concentration; 30 days inactive closes the account. Penalties include "forfeiture of rewards". FTMO may review any account.
- STILL UNCONFIRMED: 50K Growth payout cap and qualifying days ($2,500 / 5 days at $200 assumed pessimistic).
- Model implications: the pessimistic payout set's 50% matches the confirmed rule, and the funded-fee kill risk is removed. The rule-compliant cell is the one with the same sd in Eval and funded (no mismatch). S=Sf=500 gives EV +$98 per attempt (pessimistic) to +$134 (optimistic). Main residual risk: "one-sided bets / spirit" discretion. The strategy must have its own stop (not the DD) and consistent size.

## 2026-10-15 PREREG: FTMO option stress test (logged before the run)
Strategy, signal-free and rule-consistent: each weekday, a random direction at 09:00 ET with k MGC. Exit at 16:00 ET or at our own stop of -$800 (k*10*move), filled at the first 1-min close beyond it, so the bar gap counts as slippage. In funded, the stop is min($800, $1,000 soft DLL). Same k in Eval and funded.
Days: bootstrapped from REAL 2021-10..2024-12 HistData bars, 09:00-16:00 ET paths. The 2025-26 data stays sealed.
Costs: $3 per round trip per MGC (base), $6 (stress).
Payout terms, pessimistic: 50% withdrawable (confirmed), cap $2,500, 5 qualifying days at >= $200, 90% split.
k in {1,2,3,4}. Seeds 1 and 2. N = 50,000.
PASS: EV per attempt > 0 at $6 cost on both seeds for the chosen k AND for its neighbours (k±1, roughly the ±30% sd band) AND SE < 25% of EV. Otherwise the FTMO option is DEAD.
RESULT (ftmo_stress.py, 782 real days, sd $131 per MGC 09-16):
| k | sd/day | EV @$3 (s1/s2) | EV @$6 (s1/s2) | p_pass @$6 |
| 1 | 131 | -1004/-1004 | -928/-926 | 0.047 |
| 2 | 262 | -247/-245 | -291/-289 | 0.145 |
| 3 | 380 | -61/-60 | -123/-120 | 0.176 |
| 4 | 495 | -11/-12 | -61/-61 | 0.174 |
SE 2-3. VERDICT: FAIL; every cell is negative, at both seeds and both costs. The FTMO option is DEAD under the prereg.
The normal model's +$98 at sd 500 did not survive real gold paths, k-scaled costs ($12-24 per day vs $3.75 modelled), and stop slippage at the bar close.
k >= 5 (sd 600+) was not pre-registered and is NOT run: that would be fishing.

## 2026-10-15 CORRECTION (formal)
I claimed futures escape swap on multi-week holds. That is wrong in substance. A futures price embeds financing (F ≈ S·(1 + r − lease)), and the basis converges, so a long future pays about r per year exactly like a swap. Futures remove only the broker's swap MARKUP: OANDA's −5.45% long / +1.85% short implies about ±1.8% around r. They also remove the spread, and the 16:10 flat-out rule is FTMO-only. Multi-week tests must use excess returns (spot − r), not spot returns.

## PREREG: last lever, multi-week time-series momentum on gold (logged before the run)
Rule (Moskowitz-Ooi-Pedersen 2012, published, untuned): at each month-end, position = sign(12-month excess return), hold one month, 1x. Secondary rules, reported but not decision-grade: 1-month and 3-month lookbacks.
Data: XAUUSD daily 16:00 NY mid. FX-Data 2011-06..2016-12 (first 12 months are warm-up) and HistData 2021-10..2024-12 (first 12 months are warm-up). No 2025-26 data is used.
Returns: spot minus r. r = 3m T-bill annual average, hard-coded: 2011-15 0.05%, 2016 0.3%, 2021 0.05%, 2022 2.0%, 2023 5.1%, 2024 5.0%.
Costs: MGC 0.65 bp per position change, plus a 2 bp roll every 2 months while in a position. Stress 2x.
Months: about 54 + 27 = 81. MDE Sharpe ≈ 2/sqrt(6.75) ≈ 0.77.
PASS: annualized net Sharpe ≥ 0.77, net > 0 at 2x cost, and positive in both eras. FAIL closes the last lever.
RESULT (tsmom.py): 12m lookback, 81 months: gross Sharpe −0.17, net −0.18, t −0.47. Era A −16 bp/mo, era B −41 bp/mo. 3m: net Sharpe −0.55. 1m: −0.18.
VERDICT: FAIL. Gross is negative before any cost. The last lever is closed.
PROGRAM CLOSED: 32 tests (intraday, daily, multi-week, account-structure). 0 survivors. No further tests on US500/XAUUSD/GBPUSD without a new information source.

## PREREG (2026-10-15, before data): Opening-Range Breakout, fabledforman TradingView open-source (top-liked ORB). Author defaults, untuned.
Instrument: US500 via HistData SPXUSD tick bid/ask (spread median 0.63 pt in 2022-03, ~1.4 bp).
Rules: OR = 09:30-10:15 ET mid high/low. Trade only if OR width >= 0.35% of the 10:15 price. After 10:15: stop-buy at OR high, stop-sell at OR low, first touch wins.
Fill at max(level, bar open) + half spread (long; mirrored for short). Stop = 0.5 × OR width from entry. Target = 1.1 × stop distance.
On a stop-out, reverse once (same stop and target rules from the new entry), so at most 2 trades a day. Flat at 15:45 at bid/ask.
If a bar touches both stop and target, assume the STOP (conservative). 1-min bars, America/New_York.
Costs: CFD leg = actual bar spreads plus 0 commission. MES leg = flat 0.7 bp round trip. Both legs at 1x and 2x.
DEV 2021-10..2024-12. HOLDOUT 2025-01..2026-09, run once and only if DEV passes.
PASS (DEV): gross >= 2 × round-trip cost per trade; net t >= 2 (MDE Sharpe ≈ 1.12); net > 0 at 2x cost; >= 60% of years positive. Trades/week reported against the 4/week floor.
Unknowns resolved by assumption, since the Pine source was not visible: one reversal per day; the OR filter uses the 10:15 mid.
RESULT ORB DEV 2021-10..2024-12 (335 trade days):
- CFD: trades/wk 2.93, gross 3.11, cost 1.12, net +1.99 bp/trade, t 1.32, Sharpe 0.72, maxDD -6.2%, 3/4 years positive. At 2x cost: net +0.87.
- MES: net +2.41, t 1.60, Sharpe 0.87, maxDD -4.9%. At 2x cost: net +1.71.
VERDICT: FAIL. It clears the gross ≥ 2× cost bar, net > 0 at 2x and the years-positive bar, but FAILS on t (1.60 vs 2.0, MDE 1.12) and on frequency (2.93 vs 4 trades/week). Holdout NOT opened. This is the strongest near-miss in the program and is flagged for blind replication only.

## 2026-10-15 ORB blind replication (Haiku, spec only, no access to the code)
Days 335, 497 trades. Gross 3.107, cost 1.120, net 1.987, t 1.316. MES flat cost: net 2.407, t 1.600. Matches the original to 3 decimals.
Net per trade by year: 2021 +4.52, 2022 +2.51, 2023 -1.07, 2024 +2.18.
External disconfirmer (sprawl lane 17): Krueger's MQL5 replication of the Zarattini ORB on SPX CFD, 2015-2026: gross +0.119R (t 2.4), net -0.081R (t -1.6).
STATUS: confirmed DEV near-miss. It still FAILS the prereg (t, frequency). Holdout stays sealed.

## 2026-10-15 Research sprawl (20 Haiku lanes, RESEARCH_SPRAWL.md): 19 of 20 returned, all NOTHING
Rate limits thinned lanes 8 and 10. Useful facts:
- Topstep micro fees $1.22 (MES) / $1.92 (MGC) round trip. MGC all-in ≈ 0.73 bp at $4,000 gold, ≈ 1.5 bp at $1,900; MES ≈ 0.83 bp at 6,000.
- Slippage vendor claim: ~1 tick per trade (unverified).
- 43-gold-EA backtest: 19% blow-ups.
- Pre-FOMC drift, turn-of-month and VWAP reversion: no 2023+ support.
- 2025-26 papers find no intraday predictability on MNQ/SPY after costs.

## PREREG 2026-10-15: ORB forward paper test on MES (orb_paper/README.md holds the binding rules)
Window 2026-10-19..2027-01-15, 1 MES, rules unchanged. KILL: slippage > 1 tick per side, or any rule break. PASS: net > 0, all-in cost <= 1.2 bp, 100% rule adherence.
On PASS: 6 more months of paper, plus a one-shot opening of the sealed 2025-26 holdout (this is the pre-logged exception). On FAIL: ORB is dead.
