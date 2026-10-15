"""Scores the LOCKED Gao rule (see gao_hfm_spx.py) once on SPXUSD window 2018-07..2021-09."""
import glob, numpy as np, pandas as pd
from statistics import NormalDist
fs = [f for f in sorted(glob.glob('/home/user/SPX/edge/data/SPXUSD_HD_*.pkl'))
      if 201807 <= int(f.split('_')[-1][:6]) <= 202109]
b = pd.concat([pd.read_pickle(f) for f in fs]).sort_index()
b = b[~b.index.duplicated()]
loc = b.index.tz_convert('America/New_York')
df = pd.DataFrame({'c': b.c.values, 'o': b.o.values, 'spr': b.spr.values, 'hm': loc.hour * 60 + loc.minute,
                   'd': loc.date, 'wd': loc.weekday}, index=b.index)
df = df[df.wd < 5]
rows = []
for d, g in df.groupby('d'):
    g = g.set_index('hm')
    try:
        o = g.loc[570, 'o']; c10 = g.loc[600, 'c']; e = g.loc[930]; x = g.loc[960]
    except KeyError:
        continue
    r1 = c10 / o - 1
    if r1 == 0: continue
    s = 1 if r1 > 0 else -1
    gross = s * (x.c / e.c - 1) * 1e4
    spread_bp = (e.spr / e.c + x.spr / x.c) / 2 * 1e4
    rows.append((d, gross, spread_bp))
res = pd.DataFrame(rows, columns=['d', 'gross', 'spread_bp']).set_index('d')
res['net_1x'] = res.gross - (0.70 + res.spread_bp)   # MES flat RT + half-spread x2 crossings
res['net_2x'] = res.gross - 2 * (0.70 + res.spread_bp)
n = len(res)
t2 = res.net_2x.mean() / res.net_2x.std(ddof=1) * np.sqrt(n)
p2 = 1 - NormalDist().cdf(t2)
print(f'days {n}  {res.index.min()} .. {res.index.max()}')
print(f'gross {res.gross.mean():.2f} bp/day  net_1x {res.net_1x.mean():.2f}  net_2x {res.net_2x.mean():.2f}')
print(f't(net_2x) {t2:.2f}  one-sided p {p2:.4f}')
print('per year net_2x:', res.net_2x.groupby(pd.to_datetime(res.index).year).mean().round(2).to_dict())
res.to_csv('/home/user/SPX/learning/family/f1/gao_days.csv')
