"""FTMO Futures 50K Growth option value on bootstrapped REAL gold days (prereg in SEARCH_LOG 2026-10-15)."""
import sys
import numpy as np, pandas as pd
sys.path.insert(0, '/home/user/SPX/edge/scripts')
from battery import load

STOP = 800.0
b = load('XAUUSD_HD')
b = b[(b.index >= '2021-10-01') & (b.index < '2025-01-01')]
loc = b.index.tz_convert('America/New_York')
m = loc.hour * 60 + loc.minute
s = b[(m >= 539) & (m < 960) & (loc.weekday < 5)]  # bar 08:59 close = 09:00 price ... 15:59 close = 16:00
sl = s.index.tz_convert('America/New_York')
piv = pd.DataFrame({'d': sl.date, 'm': sl.hour * 60 + sl.minute - 539, 'c': s.c.values}).pivot_table(
    index='d', columns='m', values='c', aggfunc='last').reindex(columns=range(421)).ffill(axis=1)
piv = piv[piv[0].notna() & piv[420].notna()]
D = (piv.values - piv.values[:, :1]) * 10  # $ per MGC long, path
print('days', len(D), 'sd per MGC 09-16 $', round(D[:, -1].std(), 1))


def day_pnl(path, k, stop):
    p = path * k
    hit = (p <= -stop)
    first = np.where(hit.any(1), hit.argmax(1), -1)
    out = p[:, -1].copy()
    idx = first >= 0
    out[idx] = p[idx, first[idx]]  # fill at the breaching bar close (gap = slippage)
    return out


def tables(k, cost):
    ev = {}
    for stop in (STOP, min(STOP, 1000.0)):
        L = day_pnl(D, k, stop); Sh = day_pnl(-D, k, stop)
        ev[stop] = np.concatenate([L, Sh]) - cost * k
    return ev[STOP], ev[min(STOP, 1000.0)]


def attempt(k, cost, seed, N=50000, cap=2500, frac=0.5, Q=5, qmin=200):
    rng = np.random.default_rng(seed)
    E, F = tables(k, cost)
    draw = lambda T: T[rng.integers(0, len(T), N)]
    bal = np.full(N, 50000.); peak = bal.copy(); alive = np.ones(N, bool); passed = np.zeros(N, bool)
    best = np.zeros(N); days = np.zeros(N)
    for t in range(300):
        act = alive & ~passed
        if not act.any(): break
        p = np.where(act, draw(E), 0); bal += p; days += act; best = np.maximum(best, p)
        peak = np.maximum(peak, bal); alive &= bal > np.minimum(peak - 2000, 50000)
        prof = bal - 50000; passed |= act & alive & (prof >= 3000) & (best <= 0.4 * prof)
    fees = 119 * np.ceil(np.maximum(days, 1) / 21)
    pay = np.zeros(N); bb = np.full(N, 50000.); pk = bb.copy(); live = passed.copy(); q = np.zeros(N)
    for t in range(250):
        p = np.where(live, draw(F), 0); bb += p; pk = np.maximum(pk, bb)
        live &= bb > np.minimum(pk - 2000, 50000); q += live & (p >= qmin)
        prof = bb - 50000; el = live & (q >= Q) & (prof > 0)
        req = np.where(el, np.minimum(cap, frac * prof), 0); pay += 0.9 * req; bb -= req; q[el] = 0
    v = pay - fees
    return passed.mean(), fees.mean(), pay.mean(), v.mean(), v.std() / np.sqrt(N)


if __name__ == '__main__':
    print('k cost seed | sd_day  p_pass  fees  payouts  EV  SE')
    for cost in (3, 6):
        for k in (1, 2, 3, 4):
            sd = np.concatenate(tables(k, cost)[:1])[:].std()
            for seed in (1, 2):
                r = attempt(k, cost, seed)
                print(f'{k} {cost} {seed} | {sd:6.0f} {r[0]:.3f} {r[1]:5.0f} {r[2]:6.0f} {r[3]:6.0f} {r[4]:4.0f}', flush=True)
