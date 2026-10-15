"""Score the ORB MES paper log. Usage: python3 score.py"""
import pandas as pd, numpy as np
FEE = 1.22  # $ round trip per MES
d = pd.read_csv(__file__.replace('score.py', 'log.csv'), parse_dates=['date'])
if d.empty: print('no rows yet'); raise SystemExit
t = d[d.skip == 0].copy()
sgn = np.where(t.side == 'L', 1, -1)
t['gross_bp'] = sgn * (t.exit_fill_px - t.fill_px) / t.fill_px * 1e4
t['fee_bp'] = FEE / (5 * t.fill_px) * 1e4
t['net_bp'] = t.gross_bp - t.fee_bp
t['slip_in'] = sgn * (t.fill_px - t.trigger_px) / 0.25  # ticks worse than trigger
t['slip_out'] = sgn * (t.exit_model_px - t.exit_fill_px) / 0.25
t['cost_bp'] = t.fee_bp + (t.slip_in.clip(lower=0) + t.slip_out.clip(lower=0)) * 0.25 / t.fill_px * 1e4
wk = max((d.date.max() - d.date.min()).days / 7, 1)
print(f'days logged {d.date.nunique()}  trades {len(t)}  trades/wk {len(t)/wk:.2f}')
print(f'gross {t.gross_bp.mean():.2f}  net {t.net_bp.mean():.2f} bp/trade  t {t.net_bp.mean()/t.net_bp.std()*np.sqrt(len(t)) if len(t)>1 else float("nan"):.2f}')
print(f'slippage ticks/side: entry {t.slip_in.mean():.2f}  exit {t.slip_out.mean():.2f}  all-in cost {t.cost_bp.mean():.2f} bp')
kill = (t[['slip_in', 'slip_out']].mean().mean() > 1.0)
print('KILL: slippage > 1 tick/side' if kill else 'slippage OK')
print('Remember: any rule break = KILL (log it honestly).')
