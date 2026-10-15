"""Score one locked hypothesis on forward data only. Usage: python3 score_forward.py ID net_bp_per_trade_series.csv
CSV columns: date, net_bp (one row per trade day, after costs). Refuses data dated before the spec's forward_start."""
import json, sys, math, os
import pandas as pd
from statistics import NormalDist
REG = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'registry.jsonl')
rec = next(json.loads(l) for l in open(REG) if json.loads(l)['id'] == sys.argv[1])
d = pd.read_csv(sys.argv[2], parse_dates=['date'])
d = d[d.date >= pd.Timestamp(rec['forward_start'])]
assert len(d) >= 60, 'need at least 60 forward days'
n = len(d); mu = d.net_bp.mean(); sd = d.net_bp.std(ddof=1); t = mu / sd * math.sqrt(n)
p1 = 1 - NormalDist().cdf(t)
print(f"{rec['id']}: n={n} net={mu:.2f} bp/day t={t:.2f} one-sided p={p1:.4f}")
print('Pass only if p is below the Bonferroni threshold for the family size N (see correct.py).')
