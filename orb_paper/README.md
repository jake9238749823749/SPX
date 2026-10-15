# ORB paper trade on MES: forward test (pre-registered 2026-10-15)

Rules are the ones tested in edge/scripts/orb.py and blind-replicated. NOTHING changes during the test.

## Daily checklist (New York time, weekdays)
1. **09:30-10:15:** do nothing. At 10:15, read the MES 1-min (or 15-min) chart. H = highest high, L = lowest low of 09:30-10:14.
2. **Filter:** W = H - L. If W < 0.0035 × price (about 21 pts at 6,000), log "skip" and stop for the day.
3. **10:15:** place an **OCO pair**: a Buy Stop at H + 0.25 and a Sell Stop at L - 0.25. One fills, the other cancels.
4. **On fill:** attach a bracket.
   - Stop = 0.5 × W from your FILL price.
   - Target = 0.55 × W from your fill price.
   - Round both to 0.25.
5. **If stopped out:** immediately enter the OPPOSITE direction at market (once only), with a new bracket (stop 0.5 × W, target 0.55 × W from the new fill). A second stop-out means you are done for the day.
6. **15:45:** close anything open at market. Cancel unfilled orders.
7. **Log every fill** in `log.csv` (one row per trade), the same day.

Size: **1 MES**. Venue: TradingView paper, Tradovate sim, or NinjaTrader sim. Note which one in the log.
Cost assumption: fees $1.22 round trip per MES (Topstep schedule; FTMO is $0.40 plus exchange fees).

## Log format (log.csv)
date, venue, H, L, W, skip(0/1), leg(1/2), side(L/S), trigger_px, fill_px, exit_reason(stop/target/close), exit_model_px, exit_fill_px
- trigger_px = the price your stop order was set at (H+0.25 / L-0.25, or the exit level of leg 1 for leg 2)
- exit_model_px = your planned stop/target price (or the 15:45 price)
Skips get one row with skip=1.

## Scoring: run `python3 score.py`
It reports trades/week, net bp per trade after fees, average slippage in ticks (fill vs trigger, and exit fill vs model), and the kill checks.

## Pre-registered decision (fixed now; no changes later)
Window: 2026-10-19 to 2027-01-15 (13 weeks, ~35-40 trades expected).
- KILL at any time if: average slippage > 1.0 tick per side, OR any day where the rules were not followed (missed order, discretionary exit). Execution that can't follow the rules is not this strategy.
- At the end, PASS only if all three hold: net bp per trade (after real fills + fees) > 0; average all-in cost <= 1.2 bp per trade; 100% rule adherence.
- PASS does NOT mean go live. It means: continue paper for 6 more months, AND re-run the sealed 2025-26 holdout once (this forward test is the pre-logged exception that justifies opening it).
- FAIL means ORB is dead for this program.
What 13 weeks can and cannot show: it checks execution and costs. It cannot prove the edge (that needs about 2 years).
