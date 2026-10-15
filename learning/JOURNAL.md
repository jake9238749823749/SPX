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
