"""T1: 10-month SMA timing vs buy-and-hold on Shiller monthly S&P 500. One run. See PREREG.md."""
import numpy as np, pandas as pd, io, urllib.request
URL = 'https://raw.githubusercontent.com/datasets/s-and-p-500/main/data/data.csv'
d = pd.read_csv(io.StringIO(urllib.request.urlopen(URL, timeout=60).read().decode()), parse_dates=['Date']).set_index('Date')
P = d.SP500
dy = (d.Dividend / P).replace(0, np.nan).ffill()               # carry forward last D/P
rate = d['Long Interest Rate'].replace(0, np.nan).ffill() / 100
tr = P.pct_change() + dy / 12                                   # monthly total return
sig = (P > P.rolling(10).mean()).astype(float)                  # signal at month t (average-based)
pos = sig.shift(2)                                              # applies to return from t+1 to t+2
switch = pos.diff().abs().fillna(0)

def stats(lo, hi, cash):
    m = (tr.index >= lo) & (tr.index <= hi) & pos.notna() & tr.notna()
    r_bh = tr[m]; c = cash[m]
    r_t = pos[m] * r_bh + (1 - pos[m]) * c - switch[m] * 0.0002
    out = {}
    for k, r in [('buy_hold', r_bh), ('timing', r_t)]:
        eq = (1 + r).cumprod(); yrs = len(r) / 12
        cagr = eq.iloc[-1] ** (1 / yrs) - 1
        vol = r.std() * np.sqrt(12)
        sh = (r - c).mean() / (r - c).std() * np.sqrt(12)
        dd = (eq / eq.cummax() - 1).min()
        out[k] = dict(CAGR=round(cagr * 100, 2), vol=round(vol * 100, 2), Sharpe=round(sh, 2), maxDD=round(dd * 100, 1))
    out['months_invested_pct'] = round(pos[m].mean() * 100, 1)
    out['exits'] = int(((pos[m].diff()) == -1).sum())
    # block bootstrap of Sharpe difference
    rng = np.random.default_rng(0); n = len(r_bh); xb = (r_bh - c).values; xt = (r_t - c).values
    diffs = []
    for _ in range(5000):
        idx = np.concatenate([np.arange(s, s + 12) % n for s in rng.integers(0, n, n // 12 + 1)])[:n]
        a, b = xt[idx], xb[idx]
        diffs.append(a.mean() / a.std() - b.mean() / b.std())
    out['p_sharpe_timing_gt_bh'] = round(float((np.array(diffs) <= 0).mean()), 3)
    return out

for label, lo, hi in [('TEST 2007-01..2026-09', '2007-01-01', '2026-09-30'), ('REFERENCE 1901-2006', '1901-01-01', '2006-12-31')]:
    for cl, cash in [('cash=0', pd.Series(0.0, index=tr.index)), ('cash=10y/12', rate / 12)]:
        print(label, cl, stats(lo, hi, cash))
