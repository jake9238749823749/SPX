# Journal (append one entry each session: what I learned, what I got wrong, the next question)

## 2026-10-15
- Learned: the system only improves through written files. Weights don't change, so the knowledge base is the memory.
- Got wrong: I called the forecaster's baseline "fixed" when it was really a dev-period number. Corrected in system/ANALYSIS_2026-10-15.md.
- Learned: hit rate and expected value can disagree. ORB holdout had 64% profitable days and −3.4 bp average net per day.
- Next question: curriculum topic 1, microstructure. Does a limit order's expected fill beat the mid after adverse selection on MES?

## 2026-10-15 (goal: recursive loop toward a millions-per-year edge)
- Gate: $1M in one year needs 100% on $1M, 10% on $10M, 2000% on $50k. The plausible edge here is 0-10%/yr. Millions in one year is infeasible from the capital this repo assumes; no measured edge supports it.
- Built learning/LOOP.md: feasibility gate, eight-step cycle, stop conditions.
- Next question: the calibration loop Jake has not yet approved, or the CME fee page (needed to close the microstructure paper answer).

## 2026-10-15 (family goal: lock hypotheses before data, correct for N)
- Built learning/family: register.py (refuses spec without forward_start after lock date), correct.py (Bonferroni and expected-max Sharpe), score_forward.py (forward-only).
- Locked 7 specs. 3 are spent on known data and cannot pass. 4 are open for forward scoring.
- Learned: "thousands of candidates, each scored once" is not possible on data already seen. Every verdict needs forward data, which lags by months.
- Next question: a source for new hypotheses that doesn't hit search rate limits.

## 2026-10-15 (family goal, advisor-reviewed)
- Advisor flagged that "data is spent" may be false. Verified: HistData serves 2019 and 2020 windows. The GBPUSD 2018-07+ window is unspent and is the best one-shot window (DATA_LEDGER.md).
- Power table added to FAMILY.md. N=1,000 on 8 years gives minimum detectable Sharpe ≈ 1.4.
- Next: a paper gate (instrument, frequency, FTMO legality, exact parameters, 2x cost) and a harvest batch of ≤20 agents, then lock code hashes, then open GBPUSD 2018-07+ once.
- 2026-10-15: F1 paper gate: 0/7 pass; no window opened; goal not met. Needs new candidates with exact rules, >=4/wk, and 2023+ gross evidence.

## 2026-10-15 (Audit 002: Forecast-to-Fill, arXiv 2511.08571)
- Found and extracted the paper (three independent extractions, reconciled). Verdict: UNAUDITABLE as written; fails frequency (2.3/wk), the paper's own 2x-cost row (Sharpe −1.00), and the net-vs-gross headline question.
- Learned: a headline Sharpe can be a cost-free or T+0 figure. Read the cost table, not the abstract.
- Next question: none from this paper until its parameters are published; no pre-registration justified.
- 2026-10-15: Audit 002 final: 4 lenses FATAL (arith, leak, cost, replic), 2 CONCERN (freq, data). 9/11 findings survived refutation. Verdict UNAUDITABLE, fails as written.
- 2026-10-15: Audit 002 workflow stopped at user request; synthesis and two refuters not completed. Verdict stands on completed results.

## 2026-10-16 (goal change)
- Goal changed from FTMO to growing a Robinhood account (GOAL.md). The 4/week floor and the 16:10 flat rule no longer apply; costs drop to spread plus taxes.
- Next question: does any long-horizon rule beat buy-and-hold of a broad index ETF after taxes and spread?
