"""ORB (fabledforman defaults) on SPXUSD_HD. Usage: python3 orb.py dev|hold cfd|mes"""
import sys, numpy as np, pandas as pd
sys.path.insert(0, '/home/user/SPX/edge/scripts')
from battery import load
PER = {'dev': ('2021-10-01', '2024-12-31'), 'hold': ('2025-01-01', '2026-09-30')}


def run(period, mode, mult):
    b = load('SPXUSD_HD'); l = b.index.tz_convert('America/New_York')
    mm = l.hour * 60 + l.minute
    b = b[(mm >= 570) & (mm < 945) & (l.weekday < 5)].copy()
    l = b.index.tz_convert('America/New_York'); b['d'] = l.date; b['m'] = l.hour * 60 + l.minute
    lo, hi = PER[period]; rows = []
    for d, g in b.groupby('d'):
        if not (pd.Timestamp(lo) <= pd.Timestamp(d) <= pd.Timestamp(hi)): continue
        orb = g[g.m < 615]; rest = g[g.m >= 615]
        if len(orb) < 40 or len(rest) < 300: continue
        H, L = orb.h.max(), orb.l.min(); ref = orb.c.iloc[-1]; W = H - L
        if W < 0.0035 * ref: continue
        pos, ntr, gross, cost = 0, 0, 0.0, 0.0; entry = stop = tgt = None; reversed_ = False
        def c_side(spr): return (MESC / 2 * ref / 1e4 if mode == 'mes' else spr / 2) * mult
        for _, r in rest.iterrows():
            if pos == 0 and ntr == 0:
                if r.h >= H: pos, entry = 1, max(H, r.o)
                elif r.l <= L: pos, entry = -1, min(L, r.o)
                else: continue
                ntr = 1; cost += c_side(r.spr); stop = entry - pos * W * 0.5; tgt = entry + pos * W * 0.55
                continue
            if pos == 0: continue
            hit_s = (r.l <= stop) if pos > 0 else (r.h >= stop)
            hit_t = (r.h >= tgt) if pos > 0 else (r.l <= tgt)
            if hit_s:
                px = stop if (r.o - stop) * pos > 0 else r.o  # gap through stop -> open
                gross += pos * (px - entry); cost += c_side(r.spr)
                if not reversed_:
                    reversed_ = True; pos = -pos; entry = px; ntr += 1; cost += c_side(r.spr)
                    stop = entry - pos * W * 0.5; tgt = entry + pos * W * 0.55
                else: pos = 0
            elif hit_t:
                gross += pos * (tgt - entry); cost += c_side(r.spr); pos = 0
        if pos != 0:
            r = rest.iloc[-1]; gross += pos * (r.c - entry); cost += c_side(r.spr)
        if ntr: rows.append((pd.Timestamp(d), ntr, gross / ref * 1e4, cost / ref * 1e4))
    df = pd.DataFrame(rows, columns=['d', 'n', 'gross', 'cost']).set_index('d'); df['net'] = df.gross - df.cost
    return df


MESC = 0.7
if __name__ == '__main__':
    period, mode = sys.argv[1], sys.argv[2]
    for mult in (1, 2):
        df = run(period, mode, mult); n = df.n.sum(); wk = len(pd.bdate_range(*PER[period])) / 5
        yrs = df.net.groupby(df.index.year).sum()
        t = df.net.mean() / df.net.std() * np.sqrt(len(df))
        print(f'{period} {mode} x{mult}: days {len(df)} trades/wk {n/wk:.2f} gross/tr {df.gross.sum()/n:.2f} cost/tr {df.cost.sum()/n:.2f} '
              f'net/tr {df.net.sum()/n:.2f} t {t:.2f} Sharpe {df.net.mean()/df.net.std()*np.sqrt(252*len(df)/(wk*5)):.2f} '
              f'maxDD% {(df.net.cumsum()-df.net.cumsum().cummax()).min()/100:.1f} yrs+ {(yrs>0).sum()}/{len(yrs)}', flush=True)
