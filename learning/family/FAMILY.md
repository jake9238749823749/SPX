# Hypothesis family: protocol (goal: thousands of locked candidates, family-wise correction)

## Rules
1. **Lock before data.** Each hypothesis is a JSON spec registered with register.py. It gets a lock date, a SHA-256 of its canonical spec, and a forward_start strictly after the lock date. Registration refuses anything else.
2. **Forward only for any new claim.** Data we already used (dev, holdout, sealed windows listed in SEARCH_LOG.md) is marked spent_on_known_data = true. Spent hypotheses still count toward N, but they cannot pass.
3. **N counts every test ever**, including spent ones, so the correction is conservative. Current N = 7 locked here, plus 34 earlier tests logged in edge/SEARCH_LOG.md. Use N = 41 until the family is larger.
4. **Correction.** A hypothesis passes only if its one-sided forward p-value is below the Bonferroni threshold for N (correct.py N). Holm is stricter-or-equal and may be used instead. The deflated Sharpe must also exceed 0.95 against the expected maximum for N trials.
5. **Scored once.** score_forward.py reads only rows on or after forward_start. A hypothesis scored once is closed: its status is set to pass or fail, and it can't be re-run with new parameters. A changed rule is a new id.
6. **Kill condition in the spec is binding.** It's written before data, and it is checked before scoring.

## Thresholds (from correct.py)
| N | Bonferroni z | Expected max Sharpe by chance (annualised) |

Minimum detectable annualised Sharpe ≈ z(1−0.05/N)/√years. N=1,000 on 8 years ≈ 1.4; N=50 on 8 years ≈ 1.1.
|---|---|---|
| 7 | 2.69 | 0.98 |
| 41 | 3.11 | ~1.5 (approx) |
| 1,000 | 4.06 | 2.30 |
| 5,000 | 4.42 | 2.61 |

Read: at N = 1,000, a Sharpe of 2 is what pure chance produces. Any "Sharpe 2" result from a large search is noise unless it clears the forward threshold.

## Honest limits (the goal as stated cannot be fully met yet)
- **Data is partly unspent (corrected 2026-10-15).** Several windows were never used; see DATA_LEDGER.md. GBPUSD 2018-07 to 2026-09 is a valid one-shot window today. Forward testing is still needed for anything after 2026-09.
- **The data feed lags.** HistData publishes monthly. Forward scoring is one to two months behind the market.
- **Search rate limits.** During the sprawl, WebSearch hit too_many_requests repeatedly. Generating thousands of candidates needs a different source or a slower schedule.
- **Current family:** 7 locked specs, 3 spent. Four open for forward scoring. The first verdict is months away.

## Next actions (each one logged in JOURNAL.md)
1. Forward-score the four open specs as data arrives, with score_forward.py.
2. Expand the family in batches of 20-50 from new sources, each batch registered before any data access.
3. Re-run correct.py with the true N before each verdict.
