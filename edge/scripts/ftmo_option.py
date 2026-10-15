"""Is an FTMO Futures 50K Growth attempt positive-EV for a ZERO-edge trader? Rules from ftmo.com/en/futures/trading-objectives-and-rules (2026-10-15).
Eval: target +3000, EOD trailing DD 2000 locking at 50000, no daily limit, best day <= 40% of profit (non-fatal), $119/month.
Funded: same DD (fatal), soft daily stop -1000, payout 90% of request, request <= min(cap, frac*profit), needs Q days >= qmin since last payout.
Trader: zero drift; intraday random walk of 31 steps (half-hour checks), daily sd S; cost $3/MGC round trip; 1 MGC ~ $400 daily sd.
"""
import numpy as np
rng = np.random.default_rng(1)
FEE, TGT, DD, LOCK = 119, 3000, 2000, 50000
DAYS_MO = 21


def day(S, stop=None, n=None):
    steps = rng.normal(0, S / np.sqrt(31), (n, 31)).cumsum(1)
    pnl = steps[:, -1].copy()
    if stop is not None:
        hit = (steps <= -stop).any(1); pnl[hit] = -stop
    return pnl - 3 * max(1, S / 400)


def attempt(S, Sf, cap, frac, Q, qmin, N=20000, fund_days=250):
    # evaluation
    bal = np.full(N, 50000.); peak = bal.copy(); alive = np.ones(N, bool); passed = np.zeros(N, bool)
    best = np.zeros(N); days = np.zeros(N)
    for t in range(252):
        act = alive & ~passed
        if not act.any(): break
        p = day(S, n=N); p[~act] = 0
        bal += p; days += act; best = np.maximum(best, np.where(act, p, 0))
        peak = np.maximum(peak, bal); floor = np.minimum(peak - DD, LOCK)
        alive &= bal > floor
        prof = bal - 50000
        passed |= act & alive & (prof >= TGT) & (best <= 0.4 * prof)
    fees = FEE * np.ceil(days / DAYS_MO)
    # funded, fresh 50000 account
    pay = np.zeros(N); b = np.full(N, 50000.); pk = b.copy(); live = passed.copy(); q = np.zeros(N)
    for t in range(fund_days):
        p = day(Sf, stop=1000, n=N); p[~live] = 0
        b += p; pk = np.maximum(pk, b); fl = np.minimum(pk - DD, LOCK)
        live &= b > fl
        q += live & (p >= qmin)
        prof = b - 50000
        el = live & (q >= Q) & (prof > 0)
        req = np.where(el, np.minimum(cap, frac * prof), 0)
        pay += 0.9 * req; b -= req; q[el] = 0
    return passed.mean(), fees.mean(), pay.mean(), (pay - fees).mean()


if __name__ == '__main__':
    print('S_eval S_fund | p_pass  fees  payouts  EV/attempt   [cap, frac, Q, qmin]')
    for cap, frac, Q, qmin in [(2500, 0.5, 5, 200), (3000, 1.0, 4, 150)]:  # pessimistic, optimistic payout terms
        for S in [150, 300, 500, 800, 1200]:
            for Sf in [150, 300, 500]:
                r = attempt(S, Sf, cap, frac, Q, qmin)
                print(f'{S:6} {Sf:6} | {r[0]:.3f} {r[1]:6.0f} {r[2]:8.0f} {r[3]:10.0f}   {[cap, frac, Q, qmin]}', flush=True)
