"""Generic audit statistics from a per-day CSV. Used by every audit so results are computed the same way.
Input CSV columns: date (YYYY-MM-DD), trades (int), gross_bp (sum over the day), cost_bp (sum over the day).
Usage: python3 audit_stats.py days.csv [--split 2025-01-01]
Reports per split: trades/day, gross and net per trade, t-stat (per-day), max drawdown (bp), years positive, net at 2x cost.
Verdict rules are applied by the human, from TEMPLATE.md, not by this script."""
import sys
import numpy as np, pandas as pd

def stats(d):
    d = d.copy(); d['net'] = d.gross_bp - d.cost_bp
    tr = d.trades.sum(); n = len(d)
    t = d.net.mean() / d.net.std(ddof=1) * np.sqrt(n) if n > 1 and d.net.std(ddof=1) > 0 else float('nan')
    eq = d.net.cumsum(); dd = (eq - eq.cummax()).min()
    yrs = d.groupby(pd.to_datetime(d.date).dt.year).net.sum()
    return {'days': n, 'trades/day': round(tr / n, 2), 'gross/trade': round(d.gross_bp.sum() / tr, 2),
            'net/trade': round(d.net.sum() / tr, 2), 't(day)': round(t, 2), 'maxDD_bp': round(dd, 1),
            'years_pos': f"{(yrs > 0).sum()}/{len(yrs)}", 'net_2x/trade': round((d.gross_bp.sum() - 2 * d.cost_bp.sum()) / tr, 2)}

if __name__ == '__main__':
    d = pd.read_csv(sys.argv[1])
    split = sys.argv[sys.argv.index('--split') + 1] if '--split' in sys.argv else None
    if split:
        print('DEV ', stats(d[d.date < split])); print('HOLD', stats(d[d.date >= split]))
    else:
        print('ALL ', stats(d))
