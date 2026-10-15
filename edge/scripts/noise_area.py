"""Search 3: Zarattini-Aziz-Barbon noise-area intraday momentum, published rule, VM=1.
Usage: python3 noise_area.py dev|holdout [G-NA|C-NA]
"""
import sys
import numpy as np, pandas as pd
sys.path.insert(0, '/home/user/SPX/edge/scripts')
from battery import load, COMM, COST_MODE, MGC_RT_BP

COMM['US500'] = ('abs', 0.0)
CFG = {'G-NA': ('XAUUSD', 'America/New_York', '08:20', 310),
       'C-NA': ('GBPUSD', 'Europe/London', '08:00', 480),
       'U-NA': ('US500', 'America/New_York', '09:30', 390),
       'G-NA21': ('XAUUSD_HD', 'America/New_York', '08:20', 310)}
PER = {'dev': {'XAUUSD': ('2011-01-01', '2016-12-31'), 'GBPUSD': ('2007-01-01', '2016-12-31'),
               'US500': ('2021-10-14', '2024-12-31')},
       'holdout': {'XAUUSD': ('2017-01-01', '2018-06-19'), 'GBPUSD': ('2017-01-01', '2018-06-19'),
                   'US500': ('2025-01-01', '2026-10-14')},
       'dev21': {'XAUUSD_HD': ('2021-10-01', '2024-12-31')},
       'hold25': {'XAUUSD_HD': ('2025-01-01', '2026-09-30')}}


def grids(name):
    sym, tz, start, length = CFG[name]
    b = load(sym).copy()
    loc = b.index.tz_convert(tz)
    h, m = map(int, start.split(':'))
    mins = (loc.hour * 60 + loc.minute) - (h * 60 + m)  # bar start offset from session open
    b['date'] = loc.date; b['off'] = mins
    b = b[(b.off >= 0) & (b.off < length) & (pd.DatetimeIndex(loc).weekday < 5)]
    b['pv'] = b.c * b.n
    g = b.groupby('date')
    b['vwap'] = g.pv.cumsum() / g.n.cumsum()
    # value at offset T = close of bar starting at T-1 (ffill within day, max 3 min stale)
    piv = {}
    for col in ['c', 'bc', 'ac', 'vwap']:
        p = b.pivot_table(index='date', columns='off', values=col, aggfunc='last')
        p = p.reindex(columns=range(length)).ffill(axis=1, limit=3)
        piv[col] = p
    opn = b[b.off == 0].groupby('date').o.first().reindex(piv['c'].index)
    checks = list(range(30, length, 30))  # check offsets T: use bar T-1
    end = length  # close: bar length-1
    def at(col, T): return piv[col][T - 1]
    return sym, opn, checks, end, at


def run(name, period, cost_mult=1.0):
    sym, opn, checks, end, at = grids(name)
    days = opn.index
    P = pd.DataFrame({T: at('c', T) for T in checks + [end]})
    BID = pd.DataFrame({T: at('bc', T) for T in checks + [end]})
    ASK = pd.DataFrame({T: at('ac', T) for T in checks + [end]})
    VW = pd.DataFrame({T: at('vwap', T) for T in checks})
    move = P[checks].div(opn, axis=0).sub(1).abs()
    ok = move.notna().all(axis=1) & P[end].notna()
    sigma = move[ok].rolling(14, min_periods=14).mean().shift(1).reindex(move.index)  # prior 14 valid days
    prev_close = P[end][ok].shift(1).reindex(move.index)
    hi_ref = np.maximum(opn, prev_close); lo_ref = np.minimum(opn, prev_close)
    U = sigma.mul(hi_ref, axis=0) + pd.DataFrame({T: hi_ref for T in checks})
    L = pd.DataFrame({T: lo_ref for T in checks}) - sigma.mul(lo_ref, axis=0)
    k, c = COMM[sym]
    lo, hi = PER[period][sym]
    sel = (pd.to_datetime(days) >= lo) & (pd.to_datetime(days) <= hi)
    rows = []
    for d in np.array(days)[sel]:
        if np.isnan(sigma.loc[d]).any() or np.isnan(P.loc[d]).any() or np.isnan(prev_close.loc[d]): continue
        pos, entry, pnl, cost, ntr = 0, None, 0.0, 0.0, 0
        def fill(side, T):  # side +1 buy, -1 sell
            return ASK.loc[d, T] if side > 0 else BID.loc[d, T]
        ref = opn.loc[d]
        comm = (c if k == 'abs' else c * ref) * cost_mult
        mgc = COST_MODE['mode'] == 'mgc'
        def side_cost(px, mid):  # bp, one side
            if mgc: return MGC_RT_BP / 2 * cost_mult
            return (abs(px - mid) * cost_mult + comm) / ref * 1e4
        for T in checks:
            p, u, l, v = P.loc[d, T], U.loc[d, T], L.loc[d, T], VW.loc[d, T]
            want = pos
            if pos == 0:
                want = 1 if p > u else (-1 if p < l else 0)
            elif pos == 1:
                if p < l: want = -1
                elif p < max(u, v): want = 0
            else:
                if p > u: want = 1
                elif p > min(l, v): want = 0
            if want != pos:
                if pos != 0:  # close
                    px = fill(-pos, T); mid = P.loc[d, T]
                    pnl += pos * (mid - entry[1]) / ref * 1e4
                    cost += side_cost(px, mid) + entry[2]
                if want != 0:
                    px = fill(want, T); mid = P.loc[d, T]
                    entry = (T, mid, side_cost(px, mid)); ntr += 1
                pos = want
        if pos != 0:
            T = end; px = fill(-pos, T); mid = P.loc[d, T]
            pnl += pos * (mid - entry[1]) / ref * 1e4
            cost += side_cost(px, mid) + entry[2]
        rows.append((pd.Timestamp(d), ntr, pnl, cost))
    df = pd.DataFrame(rows, columns=['d', 'trades', 'gross', 'cost']).set_index('d')
    df['net'] = df.gross - df.cost
    return df


def stats(df):
    n = len(df); m = df.net.mean(); s = df.net.std(); tr = df.trades.sum()
    eq = df.net.cumsum(); dd = (eq - eq.cummax()).min()
    yrs = df.net.groupby(df.index.year).sum()
    return dict(days=n, trades_wk=round(tr / (n / 5), 2), gross_per_trade=round(df.gross.sum() / tr, 2),
                cost_per_trade=round(df.cost.sum() / tr, 2), net_per_trade=round(df.net.sum() / tr, 2),
                net_day_bp=round(m, 2), t=round(m / s * np.sqrt(n), 2), sharpe=round(m / s * np.sqrt(252), 2),
                ann_pct_1x=round(m * 252 / 100, 1), maxdd_pct_1x=round(dd / 100, 1), yrs_pos=f'{(yrs > 0).sum()}/{len(yrs)}',
                by_year=yrs.round(0).astype(int).to_dict())


if __name__ == '__main__':
    period = sys.argv[1]
    if len(sys.argv) > 2 and sys.argv[2] in ('cfd', 'mgc'):
        COST_MODE['mode'] = sys.argv.pop(2)
    for name in sys.argv[2:] or list(CFG):
        df = run(name, period)
        r = stats(df); r['net_day_2x'] = round(run(name, period, 2.0).net.mean(), 2)
        print(name, period, r, flush=True)
