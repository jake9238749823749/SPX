# Audit 002: "Forecast-to-Fill" gold trend strategy (arXiv 2511.08571, Singha, Aguilera-Toste, Lahiri)

**Verdict: UNAUDITABLE as written, and FAILS on the paper's own numbers.** Three independent extractions agree on the formulas, but the parameters needed to reproduce the result are missing or contradictory.

## 1. Claim
Out-of-sample Sharpe 2.88 and max drawdown 0.52%, "net" of 0.7 bp linear cost and square-root impact (γ = 0.02), gold futures, 2015-2025, walk-forward with 10-year training and 6-month test slices. Source: arxiv.org/abs/2511.08571

## 2. Rules (what can be copied)
- Daily. y = log P. EMA ỹ_t = λ ỹ_{t−1} + (1−λ) y_t. Slope Δỹ_t. z_t = (Δỹ_t − μ)/σ over a 10-year training window. p_trend = (clip(z,−3,3)+3)/6.
- Momentum m_t = 1{P_t / P_{t−50} > 1}. p_bull = ω p_trend + (1−ω) m_t, ω = 0.6.
- Entry: long if p_bull ≥ 0.52 and Δỹ_t > 0. Long only.
- Exits: stop at 2×ATR14 below entry; trailing stop at 1.5×ATR14 from peak; 30-day timeout; halve or close if p_bear > 0.50.
- Sizing: friction-adjusted fractional Kelly, f̃ = 0.40 f*, with k = 0.7 bp and γ = 0.02.

## 3. Missing or contradictory (blocks blind replication)
- **Not stated:** the EMA decay λ, the EWMA θ, the ω "objective", the 0.52 threshold ("empirically chosen during training" in §6.3), the trade-stop trigger (close or intraday), fill on stop days, and the n (round trips per day) used in sizing.
- **Contradictory:** whether λ, ω and the threshold are fixed or re-estimated per window (§3.4 and §6.2 say frozen; §5 lists them as training estimates); the cost basis (k per round trip or per unit of |Δw|, a factor of two); fill timing (T+0 in the headline, T+1 as baseline in the Clarifications); the data series (LBMA/COMEX settlement in the main text, CME GC front-month in the Clarifications).
- **Grid:** 64 configurations, values not given, not stated whether selected in-sample or out-of-sample.
- **Missing appendices and companion materials**; no code or data link.

## 4. Numbers that don't reconcile
- **Frequency:** 1,282 entries over 2,793 days ≈ 2.3 per week. Fails our 4-per-week floor.
- **2x cost:** Table 3 gives Sharpe −1.00 at 2x cost. The text says "close to zero".
- **Headline "net":** the zero-cost intercept in Table 3 is 2.8775, and the 1.0x row is 0.94. The 2.88 headline equals the T+0 row. It may not be net of cost.
- **43% "CAGR":** the realised return is 2.6%. The 43% comes from scaling to a 15% volatility target that is never backtested; the paper's own scaling argument breaks at that size.
- **Capacity:** the printed inputs give about $2.2M, not the $760M claimed. A 0.07% participation claim doesn't match the paper's own definitions.
- **Regression:** t-statistics imply R² ≈ 0.26, but the paper says R² ≈ 0.001.
- **Growth branch:** on the printed inputs the growth rate is negative at the stated exposures, which contradicts the claim that the strategy sits on the positive-growth branch.
- **Text damage:** §12.1 ends mid-word; Appendix C has a broken cross-reference.

## 5. Replication
Not possible from the text. The paper's fitted parameters (λ, θ, ω, threshold, grid choice) are the ones a replication must reproduce exactly, and they are not given. Any implementation would be our own variant, which is a new hypothesis, not this paper.

## 6. Data overlap (for us)
The paper's 2015-2025 window overlaps gold data we've already spent (2011-18 and 2021-26). The only unspent gold window is 2018-07 to 2021-09, which is inside the paper's period and would still not be a clean test of its fitted parameters.

## 7. Verdict
UNAUDITABLE. Even if reproduced, it fails our gate on frequency (2.3/wk), on the paper's own 2x-cost row, and on the unresolved net-vs-gross question. No pre-registration is justified from this paper.

## 8. Full audit results (workflow wf_9f3d8fe3, 6 lenses, 3 refuters per serious finding)
- **Arithmetic: FATAL.** Net status not established; the 1.0x Sharpe is 0.94 in Table 3 but "well above 2.5" in the text; T+0 vs T+1 shifts 31% of the return; the 15% sleeve is 16.5x leverage on the same series; IR inconsistent with its own definition.
- **Leakage: FATAL.** The 2.88 headline is the T+0 row (same-bar close fill); the paper's own baseline is T+1 (Sharpe 2.28). The P&L equation is never written. The only falsification test flips the sign, which validates nothing. The 43% CAGR is a hindsight rescaling by full-period volatility.
- **Cost: FATAL.** Table 3's zero-cost intercept times vol equals the headline return, so the headline reads as cost-free. Stated turnover implies costs about 15x smaller than the table. Capacity arithmetic gives about $2.2M, not $760M.
- **Replicability: FATAL.** λ and θ are never given values; sizing does not reproduce from printed inputs (f* = 1e-6 vs a reported mean of 0.0029); the data series is undetermined; the code and data are not released.
- **Frequency: CONCERN.** FTMO Futures forbids positions held past 16:10 ET, which the paper's P&L appears to violate. Holding period is not reported; the 1,282 "entries" are undefined, and turnover sits at the long-only ceiling.
- **Data: CONCERN.** Two incompatible series (LBMA/COMEX settlement vs CME front-month); no roll method; ATR exits need highs and lows the stated data don't contain; the sources are struck about 3.5 hours apart.
- **Refutation pass:** 9 of 11 findings survived 2 of 3 refuters, including the arithmetic contradictions, the T+0 vs T+1 timing, and the cost-basis conflict. The sizing-mismatch finding was refuted (the 25% baseline explains part of the gap) and is dropped.
- The workflow was stopped by the user before its synthesis step and last two refuter agents finished. The audit above rests on the 18 completed results; the stopped agents' outputs are not used.

## 9. Final verdict
UNAUDITABLE, and FAILS as written. Its headline 2.88 can't be attributed to a costed, executable, out-of-sample strategy. No pre-registration from this paper.
