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

## 8. Disconfirming evidence and limits
- Three independent extractions agree on the formulas; the failures are in the parameters and the reconciliation, not the core idea.
- The audit lenses (arithmetic, leakage, cost, frequency, replicability, data) and their refutation pass were still running when this was written. Any change from them will be added here.
