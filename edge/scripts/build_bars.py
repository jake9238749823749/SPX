"""Stream Dukascopy tick CSVs from FX-Data git branches into 1-minute bid/ask bars.

Usage: python3 build_bars.py SYMBOL YEAR [YEAR ...]
Output: /home/user/SPX/edge/data/{SYMBOL}_{YEAR}.pkl  (DataFrame indexed by UTC minute)
Columns: o,h,l,c (mid), bc, ac (bid/ask close), spr (mean spread), n (ticks)
"""
import io, os, shutil, subprocess, sys, tempfile
import numpy as np, pandas as pd

REPO = {'XAUUSD': 'https://github.com/FX-Data/FX-Data-XAUUSD-DS',
        'GBPUSD': 'https://github.com/FX-Data/FX-Data-GBPUSD-DS'}
OUT = '/home/user/SPX/edge/data'


def run(cmd, **kw):
    return subprocess.run(cmd, check=True, capture_output=True, **kw)


def bars_from_bytes(blob):
    df = pd.read_csv(io.BytesIO(blob), header=None, names=['t', 'bid', 'ask', 'bv', 'av'],
                     usecols=[0, 1, 2])
    if df.empty:
        return None
    df['t'] = pd.to_datetime(df['t'], format='%Y.%m.%d %H:%M:%S.%f', utc=True)
    df['mid'] = (df.bid + df.ask) / 2
    df['spr'] = df.ask - df.bid
    g = df.set_index('t').groupby(pd.Grouper(freq='1min'))
    b = pd.DataFrame({'o': g.mid.first(), 'h': g.mid.max(), 'l': g.mid.min(), 'c': g.mid.last(),
                      'bc': g.bid.last(), 'ac': g.ask.last(), 'spr': g.spr.mean(), 'n': g.mid.size()})
    return b[b.n > 0]


def do_year(sym, year):
    dst = f'{OUT}/{sym}_{year}.pkl'
    if os.path.exists(dst):
        print(sym, year, 'exists'); return
    tmp = tempfile.mkdtemp(prefix=f'{sym}{year}_', dir='/home/user/SPX/edge')
    try:
        run(['git', 'init', '-q', '--bare', tmp])
        run(['git', '-C', tmp, 'fetch', '-q', '--depth', '1', REPO[sym], f'{sym}-{year}'],
            env={**os.environ, 'GIT_LFS_SKIP_SMUDGE': '1'})
        names = run(['git', '-C', tmp, 'ls-tree', '-r', '--name-only', 'FETCH_HEAD']).stdout.decode().split()
        names = sorted(n for n in names if n.endswith('_ticks.csv'))
        # batch read blobs
        p = subprocess.Popen(['git', '-C', tmp, 'cat-file', '--batch'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        parts, chunk = [], []
        for i, n in enumerate(names):
            p.stdin.write(f'FETCH_HEAD:{n}\n'.encode()); p.stdin.flush()
            hdr = p.stdout.readline().split()
            size = int(hdr[2]); data = p.stdout.read(size); p.stdout.read(1)
            chunk.append(data if data.endswith(b'\n') else data + b'\n')
            if len(chunk) >= 200 or i == len(names) - 1:
                b = bars_from_bytes(b''.join(chunk)); chunk = []
                if b is not None: parts.append(b)
        p.stdin.close(); p.wait()
        bars = pd.concat(parts).sort_index()
        bars = bars[~bars.index.duplicated()]
        bars.to_pickle(dst)
        print(sym, year, len(names), 'files', len(bars), 'bars', 'median mid', round(bars.c.median(), 5),
              'median spr', round(bars.spr.median(), 6), flush=True)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == '__main__':
    sym = sys.argv[1]
    for y in sys.argv[2:]:
        do_year(sym, int(y))
