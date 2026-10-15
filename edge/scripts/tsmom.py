"""Prereg 2026-10-15: monthly TSMOM on gold, excess returns, MGC costs. Usage: python3 tsmom.py"""
import sys, numpy as np, pandas as pd
sys.path.insert(0, '/home/user/SPX/edge/scripts')
from battery import load
R = {2011: .0005, 2012: .0005, 2013: .0005, 2014: .0005, 2015: .0005, 2016: .003, 2021: .0005, 2022: .02, 2023: .051, 2024: .05}


def daily(sym, lo, hi):
    b = load(sym); l = b.index.tz_convert('America/New_York')
    s = b[(l.hour == 15) & (l.minute == 59)]
    s.index = s.index.tz_convert('America/New_York').normalize().tz_localize(None)
    return s.c[(s.index >= lo) & (s.index <= hi)]


def era(px):
    m = px.resample('ME').last().dropna()
    ret = m.pct_change()
    rf = pd.Series([R[d.year] / 12 for d in ret.index], index=ret.index)
    ex = ret - rf
    out = {}
    for L in (12, 3, 1):
        look = (1 + ex).rolling(L).apply(np.prod, raw=True) - 1
        pos = np.sign(look).shift(1)
        df = pd.DataFrame({'pos': pos, 'ex': ex}).dropna()
        df = df[df.index >= m.index[0] + pd.offsets.MonthEnd(12)]  # common 12m warmup
        chg = df.pos.diff().abs().fillna(1) / 2  # 1 per side change, flip = 2 sides
        roll = (df.pos != 0) * (2e-4 / 2)  # 2 bp every 2 months
        for k in (1, 2):
            cost = k * (chg * 0.65e-4 * 2 / 2 * 2 / 2 + roll)  # 0.65 bp per position change (round trip per flip leg)
            out[(L, k)] = df.pos * df.ex - cost
        out[(L, 'g')] = df.pos * df.ex
    return out


A = era(daily('XAUUSD', '2011-01-01', '2016-12-31'))
B = era(daily('XAUUSD_HD', '2021-10-01', '2024-12-31'))
print('L | months | gross Sharpe | net Sharpe 1x | net 2x mean bp/mo | eraA net bp/mo | eraB net bp/mo | t')
for L in (12, 3, 1):
    g = pd.concat([A[(L, 'g')], B[(L, 'g')]]); n1 = pd.concat([A[(L, 1)], B[(L, 1)]]); n2 = pd.concat([A[(L, 2)], B[(L, 2)]])
    sh = lambda x: x.mean() / x.std() * np.sqrt(12)
    print(L, len(n1), round(sh(g), 2), round(sh(n1), 2), round(n2.mean() * 1e4, 1), round(A[(L, 1)].mean() * 1e4, 1),
          round(B[(L, 1)].mean() * 1e4, 1), round(n1.mean() / n1.std() * np.sqrt(len(n1)), 2))
