# Pre-registration: Gold at micro-futures cost (logged 2026-10-15, before any data)
Rules (published params, untuned): (1) Zarattini-Aziz-Barbon noise-area, COMEX day session 08:20-13:30 NY; (2) PM/AM fix fade; (3) COMEX open-to-close momentum.
Data: XAUUSD 1-min bid/ask, Dukascopy export, 2021-10..2026-10. Coverage check (days present/expected) logged before results.
Costs: CFD = actual bid/ask at fill minute; MGC = 0.65 bp RT (unverified vs CME fee page); stress 2x. No swap (flat by 16:10 ET).
DEV 2021-10..2024-12 (~3.2 yr): pass = gross >= 1.4 bp/trade AND net t >= 2 AND net > 0 at 2x cost. MDE Sharpe ~ 2/sqrt(3.2) = 1.12 ann.
HOLDOUT 2025-01..2026-10 (~1.8 yr), run once: MDE Sharpe ~ 1.49; pass = net > 0 at 1x and 2x, same sign as DEV.
Nulls: sign-flip on gross (gross edge exists); recentered block bootstrap (net edge).
Kill: all three gross < 1.4 bp in DEV -> close intraday program; no 24th rule.

Amendment 2026-10-15 (before data): adopt HANDOFF.md section 4 bar exactly. DEV also needs >= 60% of years positive. HOLDOUT pass = net > 0 with one-sided p < 0.10. Where the two documents differ, HANDOFF.md governs; it was logged first.

Amendment 2 (2026-10-15, before any 2021+ result): DATA SOURCE CHANGE. Using HistData.com XAUUSD tick bid/ask (fetched via philipperemy/FX-1-Minute-Data), not a Dukascopy export.
Timestamps are fixed EST (UTC-5); converted to UTC. Bars: edge/data/XAUUSD_HD_YYYYMM.pkl, same columns as build_bars.py.
The CFD cost leg now measures HistData's feed spread (median 0.396 $ in 2022-03, about 2 bp), not Dukascopy's or TradeLocker's. Treat the CFD column as indicative only. The decision uses the MGC flat 0.65 bp leg plus 2x stress, as pre-set.
MGC cost leg: flat 0.65 bp round trip per trade, charged at mid fills (half per side); 2x = 1.30 bp.
Coverage check before results: count valid session days per month and log it.
