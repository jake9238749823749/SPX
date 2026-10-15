# Data ledger: what has been looked at (updated 2026-10-15)
"Spent" = used by a test in edge/SEARCH_LOG.md (any dev, holdout, sealed or daily window). A spent window can't pass a new hypothesis.
"Unspent" = never used by any test. Availability checked by a one-month HistData download (2026-10-15).

| Instrument | Window | Status | Evidence |
|---|---|---|---|
| XAUUSD | 2011-01..2016-12 | SPENT | G-NA dev, battery dev, daily 2011-16 |
| XAUUSD | 2017-01..2018-06 | SPENT | battery sealed (all 14 rules) |
| XAUUSD | 2018-07..2021-09 | **UNSPENT** | HistData 2019-03 and 2016-06 downloaded fine; 2018-07+ not yet probed |
| XAUUSD | 2021-10..2024-12 | SPENT | gold DEV 2021-24 |
| XAUUSD | 2025-01..2026-09 | SPENT | holdout (gold 2025-26 used for TSMOM and DEV-only checks) |
| SPXUSD | 2019-03 and earlier | **UNSPENT** | HistData 2019-03 downloaded fine; earliest year not probed |
| SPXUSD | 2021-10..2024-12 | SPENT | ORB dev, U-NA dev |
| SPXUSD | 2025-01..2026-09 | SPENT | ORB holdout, U-NA holdout |
| GBPUSD | 2007..2016 | SPENT | daily D1-3 dev, battery dev, C-NA dev |
| GBPUSD | 2017-01..2018-06 | SPENT | battery sealed (F3b) |
| GBPUSD | 2018-07..2026-09 | **UNSPENT** | HistData 2020-03 downloaded fine; full window never used |

## What this means
- **Unspent historical windows exist** and can host a one-shot family test right now: GBPUSD 2018-07 to 2026-09 (8+ years), XAUUSD 2018-07 to 2021-09 (3 years), SPXUSD before 2021-10.
- **Contamination:** we have not looked at these windows through a rule, but any literature rule was chosen with knowledge of how these years played out. Historical scoring is valid only for rules whose exact parameters are published and fixed before this file was written. Invented variants are forward-only.
- **Recommended window:** GBPUSD 2018-07..2026-09 for the family, because it is the longest unspent window and matches the 8+ years needed for a power of about 1.2 at N = 1,000 (see FAMILY.md power table).
