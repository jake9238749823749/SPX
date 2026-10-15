"""Download HistData XAUUSD tick (bid/ask) monthly zips and build 1-min bars in the build_bars.py format.

Usage: python3 histdata_bars.py YYYYMM YYYYMM   (inclusive range)
Source timestamps are fixed EST (UTC-5, no DST). Verified from the daily-break shift at the 2022-03-13 DST change.
Output: data/XAUUSD_HD_{YYYYMM}.pkl. Columns o,h,l,c (mid), bc, ac, spr, n (ticks). Index = UTC bar start.
"""
import os, sys, zipfile
import pandas as pd
sys.path.insert(0, '/tmp/fx1m')
from histdata.api import download_hist_data, TimeFrame, Platform

OUT = '/home/user/SPX/edge/data'
ZDIR = f'{OUT}/histdata/' + str(os.getpid())  # per-process dir: no zip collisions
os.makedirs(ZDIR, exist_ok=True)


def month(ym):
    dst = f'{OUT}/XAUUSD_HD_{ym}.pkl'
    if os.path.exists(dst): return
    z = download_hist_data(year=ym[:4], month=int(ym[4:]), pair='xauusd', time_frame=TimeFrame.TICK_DATA,
                           platform=Platform.GENERIC_ASCII, output_directory=ZDIR, verbose=False)
    with zipfile.ZipFile(z) as zf:
        name = [n for n in zf.namelist() if n.endswith('.csv')][0]
        parts = []
        for df in pd.read_csv(zf.open(name), header=None, names=['t', 'bid', 'ask', 'v'], usecols=[0, 1, 2],
                              chunksize=2_000_000, dtype={'t': str}):
            df['t'] = pd.to_datetime(df.t, format='%Y%m%d %H%M%S%f') + pd.Timedelta(hours=5)
            df['t'] = df.t.dt.tz_localize('UTC')
            df['mid'] = (df.bid + df.ask) / 2; df['spr'] = df.ask - df.bid
            g = df.set_index('t').groupby(pd.Grouper(freq='1min'))
            parts.append(pd.DataFrame({'o': g.mid.first(), 'h': g.mid.max(), 'l': g.mid.min(), 'c': g.mid.last(),
                                       'bc': g.bid.last(), 'ac': g.ask.last(), 'sprsum': g.spr.sum(),
                                       'n': g.mid.size()}))
    b = pd.concat(parts); b = b[b.n > 0]
    # merge minutes split across chunk boundaries
    b = b.groupby(level=0).agg(o=('o', 'first'), h=('h', 'max'), l=('l', 'min'), c=('c', 'last'), bc=('bc', 'last'),
                               ac=('ac', 'last'), sprsum=('sprsum', 'sum'), n=('n', 'sum'))
    b['spr'] = b.sprsum / b.n; b = b.drop(columns='sprsum')[['o', 'h', 'l', 'c', 'bc', 'ac', 'spr', 'n']]
    b.to_pickle(dst); os.remove(z)
    print(ym, len(b), 'bars', 'median mid', round(b.c.median(), 2), 'median spr', round(b.spr.median(), 3), flush=True)


if __name__ == '__main__':
    a, z = pd.Period(sys.argv[1][:4] + '-' + sys.argv[1][4:], 'M'), pd.Period(sys.argv[2][:4] + '-' + sys.argv[2][4:], 'M')
    ps = list(pd.period_range(a, z, freq='M'))
    if sys.argv[3:] == ['rev']: ps = ps[::-1]  # second worker walks backward to avoid collisions
    for p in ps:
        try: month(p.strftime('%Y%m'))
        except Exception as e: print(p, 'FAIL', repr(e)[:200], flush=True)
