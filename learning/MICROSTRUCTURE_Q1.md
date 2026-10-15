# Q1 (paper answer): does a retail limit order earn the spread on MES or MGC?
- MES: 1 tick = 0.25 pt × $5 = $1.25. A perfect round trip earns at most 1 tick = $1.25, before adverse selection.
- Fees: $1.22 round trip (Topstep schedule, sprawl lane 14, unverified whether per side or round turn). If per side, $2.44 > $1.25: negative before any adverse selection.
- MGC: 1 tick = $1.00. Fees $1.92 round trip (same source). Negative even at the best possible fill.
- Adverse selection only makes it worse: passive fills happen most when price moves against you.
- Could flip: fees are lower than the Topstep schedule (e.g., per-side misread as round turn is a lower bound on fees, not an upper bound), or a rebate tier exists. Check the CME fee page first; it was 503 during our check.
- Verdict (paper): no retail edge from passive fills on these contracts unless fees are under about $1.00 round trip. Test with a real fill log before concluding more.
