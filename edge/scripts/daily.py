"""Search 2: daily-hold strategies. Usage: python3 daily.py dev|holdout [names...]"""
import sys
import numpy as np, pandas as pd
sys.path.insert(0, '/home/user/SPX/edge/scripts')
from battery import load, at, COMM

NY = 'America/New_York'
SWAP = {'GBPUSD': (-0.0108, -0.0084), 'XAUUSD': (-0.0545, 0.0185)}  # (long, short) per year
PER = {'dev': {'GBPUSD': ('2007-01-01', '2016-12-31'), 'XAUUSD': ('2011-01-01', '2016-12-31')},
       'holdout': {'GBPUSD': ('2017-01-01', '2018-06-19'), 'XAUUSD': ('2017-01-01', '2018-06-19')}}
S = {f'{k}_{s[:3]}': (s, k) for s in ['GBPUSD', 'XAUUSD'] for k in ['D1', 'D2', 'D3']}
LOOK = {'D1': 20, 'D2': 60}


def closes(sym):
    b = load(sym)
    loc = b.index.tz_convert(NY)
    days = pd.Index(sorted(set(loc.date)))
    days = pd.Index([d for d in days if pd.Timestamp(d).weekday() < 5])
    px = at(b, NY, '16:00', days).dropna()
    px.index = pd.to_datetime(px.index)
    return px


_px = {}


def run(name, period, cost_mult=1.0):
    sym, kind = S[name]
    if sym not in _px: _px[sym] = closes(sym)
    px = _px[sym]
    r = px.mid.pct_change() * 1e4
    if kind in LOOK:
        pos = np.sign(px.mid / px.mid.shift(LOOK[kind]) - 1)
    else:
        pos = -np.sign(r)
    pos = pos.fillna(0)
    # pnl on day t from position set at t-1
    held = pos.shift(1).fillna(0)
    gross = held * r
    half = (px.ask - px.bid) / 2 / px.mid * 1e4
    k, c = COMM[sym]
    comm = c / px.mid * 1e4 if k == 'abs' else c * 1e4
    trade_cost = (pos - pos.shift(1).fillna(0)).abs() * (half + comm) * cost_mult  # charged on day position is set
    nights = pd.Series(px.index, index=px.index).diff().dt.days.fillna(1)
    lr, sr = SWAP[sym]
    swap = np.where(held > 0, lr, np.where(held < 0, sr, 0)) / 365 * nights * 1e4
    net = gross - trade_cost.shift(1).fillna(0) + swap  # entry cost lands with the first day's pnl
    df = pd.DataFrame({'pos': held, 'gross': gross, 'net': net, 'cost': trade_cost.shift(1).fillna(0), 'swap': swap})
    lo, hi = PER[period][sym]
    return df.loc[lo:hi].iloc[1:]


def stats(df):
    n = len(df); m = df.net.mean(); s = df.net.std()
    eq = df.net.cumsum(); dd = (eq - eq.cummax()).min()
    yrs = df.net.groupby(df.index.year).sum()
    ch = (df.pos.diff().abs() > 0).sum() / (n / 5)
    return dict(days=n, changes_wk=round(ch, 2), gross_bp=round(df.gross.mean(), 2), cost_bp=round(df.cost.mean(), 2),
                swap_bp=round(df.swap.mean(), 2), net_bp=round(m, 2), t=round(m / s * np.sqrt(n), 2),
                sharpe=round(m / s * np.sqrt(252), 2), ann_pct=round(m * 252 / 100, 1), maxdd_pct=round(dd / 100, 1),
                yrs_pos=f'{(yrs > 0).sum()}/{len(yrs)}')


def maxt_boot(res, n_iter=2000, block=10, seed=3):
    M = pd.concat({k: v.net for k, v in res.items()}, axis=1)
    X = M.values; mu = np.nanmean(X, 0); Xc = X - mu
    real = mu / np.nanstd(X, 0) * np.sqrt((~np.isnan(X)).sum(0))
    T = len(X); rng = np.random.default_rng(seed); mx = np.empty(n_iter)
    for i in range(n_iter):
        st = rng.integers(0, T - block, T // block + 1)
        idx = (st[:, None] + np.arange(block)).ravel()[:T]
        Y = Xc[idx]; c = (~np.isnan(Y)).sum(0)
        mx[i] = np.nanmax(np.nanmean(Y, 0) / np.nanstd(Y, 0) * np.sqrt(c))
    return {k: round((np.sum(mx >= real[j]) + 1) / (n_iter + 1), 4) for j, k in enumerate(M.columns)}


if __name__ == '__main__':
    period = sys.argv[1]; names = sys.argv[2:] or list(S)
    res = {k: run(k, period) for k in names}
    rows = []
    for k in names:
        rows.append({'strat': k, **stats(res[k]), 'net_2x': round(run(k, period, 2.0).net.mean(), 2)})
    out = pd.DataFrame(rows).set_index('strat')
    if period == 'dev': out['p_adj'] = pd.Series(maxt_boot(res))
    pd.set_option('display.width', 220); print(out.to_string())
