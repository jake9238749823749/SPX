# Audit template (for any strategy, EA, script or prop-firm claim)
1. **Claim:** the exact number and source, quoted.
2. **Rules:** every parameter, copied from source. If the rules can't be copied, the audit stops here: "unauditable".
3. **Instrument and venue:** the traded product, not a proxy. Note any proxy.
4. **Data:** source, period, timezone, coverage (days per month).
5. **Costs:** bid/ask at fill minute plus commissions and fees, at 1x and 2x.
6. **Split:** pre-registered development period and holdout. Note any post-hoc exception.
7. **Results:** trades/week, gross, cost, net per trade, t-stat, max drawdown, years positive. Per-year table.
8. **Robustness:** only the published parameters. Any parameter sweep is labelled "not selection".
9. **Replication:** blind, from the written spec, or "not replicated".
10. **Verdict:** PASS / FAIL / UNAUDITABLE, with the single strongest reason.
11. **Disconfirming evidence:** the best argument the verdict is wrong.
