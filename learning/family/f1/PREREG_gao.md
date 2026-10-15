# Pre-registration: Gao rule on unspent SPX window (logged 2026-10-15 BEFORE any data download)
Amendment approved by Jake 2026-10-15: published-rule candidates may be scored on an unspent historical window. Contamination caveat: the rule was chosen with knowledge of the literature, and the scoring window was chosen knowing these years. This is a historical result, not forward evidence.
Hypothesis: first half-hour return sign predicts last half-hour return sign on the S&P 500 index.
Family for correction: N = 1 (only this hypothesis scored on window W).
PASS: net > 0 at 2x MES cost AND one-sided t-test p < 0.05 on daily net bp.
FAIL: anything else. Result is logged whether pass or fail. One scoring run only.
Kill: any rule change after this commit voids the test.
