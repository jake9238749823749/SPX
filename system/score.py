"""Deterministic scorer. Usage: python3 system/score.py
Fetches missing SPXUSD months via HistData, computes ORB day outcomes, and scores every forecast version vs P0."""
import glob, json, os, subprocess, sys
import numpy as np, pandas as pd
ROOT = os.path.dirname(os.path.abspath(__file__)); EDGE = os.path.join(ROOT, '..', 'edge', 'scripts')
sys.path.insert(0, EDGE)
P0 = 0.7254
rows = [json.loads(l) for f in sorted(glob.glob(f'{ROOT}/forecasts/*.jsonl')) for l in open(f) if l.strip()]
if not rows: print('no forecasts yet'); raise SystemExit
fc = pd.DataFrame(rows); fc['date'] = pd.to_datetime(fc.date)
if not os.path.exists('/tmp/fx1m'):
    subprocess.run(['git', 'clone', '-q', '--depth', '1', 'https://github.com/philipperemy/FX-1-Minute-Data', '/tmp/fx1m'])
for m in sorted(set(fc.date.dt.strftime('%Y%m'))):
    subprocess.run([sys.executable, f'{EDGE}/histdata_bars.py', m, m], env={**os.environ, 'PAIR': 'SPXUSD'})
import orb
orb.PER['live'] = (str(fc.date.min().date()), str(fc.date.max().date()))
out = orb.run('live', 'mes', 1); out2 = orb.run('live', 'mes', 2)
out.index = pd.to_datetime(out.index); out2.index = pd.to_datetime(out2.index)
y = (out.net > 0).astype(float).rename('y'); net2 = out2.net.rename('net2')
s = fc.merge(y, left_on='date', right_index=True).merge(net2, left_on='date', right_index=True)
rng = np.random.default_rng(0)
for v, g in s.groupby('version'):
    b = (g.p - g.y) ** 2; b0 = (P0 - g.y) ** 2; d = b0 - b
    boot = [d.values[rng.integers(0, len(d), len(d))].mean() for _ in range(5000)]
    veto = g.net2.where(g.p >= 0.5, 0).mean() - g.net2.mean()
    print(f'{v}: scored {len(g)}  Brier {b.mean():.4f} vs P0 {b0.mean():.4f}  skill {d.mean():.4f} '
          f'CI95 [{np.percentile(boot,2.5):.4f},{np.percentile(boot,97.5):.4f}]  p_sd {g.p.std():.3f}  veto_gain_2x {veto:.2f} bp/day')
