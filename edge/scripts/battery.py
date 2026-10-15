"""Run the 14 preset strategies from SEARCH_LOG.md on DEV or SEALED.

Usage: python3 battery.py dev|sealed [names...]
"""
import glob, sys
import numpy as np, pandas as pd

DATA = '/home/user/SPX/edge/data'
LON, NY = 'Europe/London', 'America/New_York'
COMM = {'GBPUSD': ('abs', 0.000025), 'XAUUSD': ('pct', 0.00002), 'XAUUSD_HD': ('pct', 0.00002)}
MGC_RT_BP = 0.65  # flat round trip for the MGC cost leg (prereg amendment 2)
COST_MODE = {'mode': 'cfd'}  # 'cfd' = bid/ask + commission; 'mgc' = flat MGC_RT_BP per trade
PERIOD = {'dev': ('2011-01-01', '2016-12-31'), 'sealed': ('2017-01-01', '2018-06-19'),
          'dev21': ('2021-10-01', '2024-12-31'), 'hold25': ('2025-01-01', '2026-09-30')}

# name: (sym, tz, signal window or None, mode, trade window)
# mode: 'fade' / 'follow' use signal sign; 'long' / 'short' fixed.
S = {
    'X1a': ('XAUUSD', LON, ('14:30', '15:00'), 'fade', ('15:05', '15:35')),
    'X1b': ('XAUUSD', LON, ('14:30', '15:00'), 'fade', ('15:05', '16:30')),
    'X2a': ('XAUUSD', LON, ('10:00', '10:30'), 'fade', ('10:35', '11:05')),
    'X2b': ('XAUUSD', LON, ('10:00', '10:30'), 'fade', ('10:35', '12:00')),
    'X3a': ('XAUUSD', LON, None, 'long', ('01:00', '07:00')),
    'X3b': ('XAUUSD', NY, None, 'short', ('09:30', '16:00')),
    'X4a': ('XAUUSD', NY, ('08:20', '08:50'), 'follow', ('13:00', '13:30')),
    'X4b': ('XAUUSD', NY, ('08:20', '08:50'), 'follow', ('12:30', '13:30')),
    'F1a': ('GBPUSD', LON, ('15:30', '16:00'), 'fade', ('16:05', '16:35')),
    'F1b': ('GBPUSD', LON, ('15:30', '16:00'), 'fade', ('16:05', '17:30')),
    'F2a': ('GBPUSD', LON, ('15:00', '15:30'), 'follow', ('15:30', '16:00')),
    'F3a': ('GBPUSD', LON, None, 'short', ('08:00', '12:00')),
    'F3b': ('GBPUSD', NY, None, 'long', ('11:00', '16:00')),
    'F4a': ('GBPUSD', LON, ('07:00', '08:00'), 'follow', ('15:00', '16:00')),
}

_cache = {}


def load(sym):
    if sym not in _cache:
        if sym.endswith('_HD'):
            fs = sorted(glob.glob(f'{DATA}/{sym}_*.pkl'))
        else:
            fs = sorted(f for f in glob.glob(f'{DATA}/{sym}_*.pkl') if '_HD_' not in f)
        b = pd.concat([pd.read_pickle(f) for f in fs]).sort_index()
        b = b[~b.index.duplicated()]
        _cache[sym] = b
    return _cache[sym]


def at(b, tz, hhmm, days):
    """Bar close (mid, bid, ask) at local time hhmm for each local date, within 3 min before."""
    h, m = map(int, hhmm.split(':'))
    ts = pd.DatetimeIndex([pd.Timestamp(d).tz_localize(tz) + pd.Timedelta(hours=h, minutes=m)
                           for d in days]).tz_convert('UTC') - pd.Timedelta(minutes=1)  # bar labelled by start
    idx = b.index.get_indexer(ts, method='ffill')
    ok = idx >= 0
    out = pd.DataFrame(index=days, columns=['mid', 'bid', 'ask'], dtype=float)
    sel = b.iloc[idx[ok]]
    lag = (ts[ok] - sel.index).total_seconds()
    good = lag <= 180
    vals = np.full((len(days), 3), np.nan)
    rows = np.where(ok)[0][good]
    vals[rows] = sel[['c', 'bc', 'ac']].values[good]
    out[:] = vals
    return out


def trades(name, period, cost_mult=1.0):
    sym, tz, sw, mode, tw = S[name]
    if period in ('dev21', 'hold25') and sym == 'XAUUSD': sym = 'XAUUSD_HD'
    b = load(sym)
    lo, hi = PERIOD[period]
    loc = b.index.tz_convert(tz)
    days = pd.Index(sorted(set(loc[(loc >= pd.Timestamp(lo, tz=tz)) & (loc <= pd.Timestamp(hi, tz=tz) + pd.Timedelta(days=1))].date)))
    days = pd.Index([d for d in days if pd.Timestamp(d).weekday() < 5])
    if sw:
        s0, s1 = at(b, tz, sw[0], days), at(b, tz, sw[1], days)
        sig = np.sign(s1.mid - s0.mid)
        d = -sig if mode == 'fade' else sig
    else:
        d = pd.Series(1.0 if mode == 'long' else -1.0, index=days)
    e, x = at(b, tz, tw[0], days), at(b, tz, tw[1], days)
    gross = d * (x.mid - e.mid) / e.mid * 1e4  # bp, mid to mid
    half_spr = ((e.ask - e.bid) / 2 + (x.ask - x.bid) / 2) / e.mid * 1e4
    kind, c = COMM[sym]
    comm = 2 * (c / e.mid * 1e4 if kind == 'abs' else c * 1e4)
    cost = (half_spr + comm) * cost_mult
    if COST_MODE['mode'] == 'mgc':
        cost = pd.Series(MGC_RT_BP * cost_mult, index=days)
    df = pd.DataFrame({'dir': d, 'gross': gross, 'cost': cost})
    df = df[(df.dir != 0) & df.gross.notna() & df.cost.notna()]
    df['net'] = df.gross - df.cost
    df.index = pd.to_datetime(df.index)
    return df


def stats(df):
    n = len(df); m = df.net.mean(); s = df.net.std()
    eq = df.net.cumsum(); dd = (eq - eq.cummax()).min()
    yrs = df.net.groupby(df.index.year).mean()
    return dict(n=n, per_wk=round(n / ((df.index[-1] - df.index[0]).days / 7), 2),
                gross=round(df.gross.mean(), 2), cost=round(df.cost.mean(), 2), net=round(m, 2),
                t=round(m / s * np.sqrt(n), 2), hit=round((df.net > 0).mean(), 3),
                maxdd_bp=round(dd, 0), yrs_pos=f'{(yrs > 0).sum()}/{len(yrs)}')


def flip_test(tr, n_iter=2000, seed=7):
    """Day-level sign flip of gross, shared across strategies; cost re-applied. max-t null."""
    allday = sorted(set().union(*[set(t.index) for t in tr.values()]))
    rng = np.random.default_rng(seed)
    real = {k: t.net.mean() / t.net.std() * np.sqrt(len(t)) for k, t in tr.items()}
    pos = {k: pd.Index(allday).get_indexer(t.index) for k, t in tr.items()}
    mx = np.empty(n_iter)
    for i in range(n_iter):
        f = rng.choice([-1.0, 1.0], len(allday))
        best = -np.inf
        for k, t in tr.items():
            net = t.gross.values * f[pos[k]] - t.cost.values
            best = max(best, net.mean() / net.std() * np.sqrt(len(net)))
        mx[i] = best
    return {k: round((np.sum(mx >= v) + 1) / (n_iter + 1), 4) for k, v in real.items()}


if __name__ == '__main__':
    period = sys.argv[1]
    if len(sys.argv) > 2 and sys.argv[2] in ('cfd', 'mgc'):
        COST_MODE['mode'] = sys.argv.pop(2)
    names = sys.argv[2:] or list(S)
    tr = {k: trades(k, period) for k in names}
    rows = []
    for k in names:
        r = stats(tr[k]); r['net_2x'] = round(trades(k, period, 2.0).net.mean(), 2); rows.append({'strat': k, **r})
    p = flip_test(tr)
    out = pd.DataFrame(rows).set_index('strat'); out['p_adj'] = pd.Series(p)
    pd.set_option('display.width', 200)
    print(out.to_string())
