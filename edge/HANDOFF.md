# Edge search: handoff (2026-10-14)

Owner: Jake. Retail systematic trader on TradeLocker, pursuing an FTMO US funded account.
Goal: one tradeable edge, or proof that none exists at this cost tier.
Full chronological record: SEARCH_LOG.md. It is append-only and includes every amendment.

## 1. Program state

- 23 strategies tested with real bid/ask data. 0 survivors.
- The constraint that binds is per-trade gross move divided by round-trip cost, not idea quality.
  - Public intraday effects are worth 0-4 bp gross per trade.
  - Published effects decay toward zero after publication.
- The only open path is gold at FTMO Futures micro-gold (MGC) cost. That is about 0.65 bp round trip, against 2.8 bp on the gold CFD.
- Kill condition for the whole intraday program: if gold gross is below 1.4 bp/trade over 2021-10 to 2024-12, close it.

Hard constraints:
- Instruments: US500, XAUUSD, GBPUSD, or their CME futures.
- At least 4 trades per week.
- No leverage or annual-return claims until a candidate passes DEV, holdout, and blind replication. Report unlevered (1x) only.
- Excluded sources:
  - SPY order-book imbalance. VWAP Reclaim, VOPRA, and SPY500-EVO are all this one bet.
  - GEX / dealer gamma.

## 2. All 23 results

Units: bp. Fills at bid/ask, plus commission (GBPUSD 0.25 pip per side; XAUUSD 0.002% per side; US500 0).

### Search 1: intraday timing, DEV 2011-16 (GBPUSD 2011-16)

Per trade. p_adj comes from a day-level sign-flip max-t test over all 14 rules. It tests gross edge, not net.

| Rule | Trades/wk | Gross | Cost | Net | t | Years + | Net at 2x cost | p_adj |
|---|---|---|---|---|---|---|---|---|
| X1a PM fix fade 15:05-15:35 | 4.95 | -0.34 | 2.71 | -3.05 | -5.09 | 0/6 | -5.76 | 1.00 |
| X1b PM fix fade 15:05-16:30 | 4.94 | 1.16 | 2.72 | -1.56 | -1.64 | 1/6 | -4.28 | 0.96 |
| X2a AM fix fade 10:35-11:05 | 4.95 | 0.67 | 2.74 | -2.07 | -6.07 | 0/6 | -4.82 | 1.00 |
| X2b AM fix fade 10:35-12:00 | 4.95 | 0.00 | 2.76 | -2.76 | -4.86 | 0/6 | -5.52 | 1.00 |
| X3a gold long 01:00-07:00 London | 3.07 | 1.81 | 3.10 | -1.29 | -0.85 | 1/6 | -4.40 | 0.64 |
| X3b gold short 09:30-16:00 NY | 4.80 | 0.94 | 2.87 | -1.93 | -1.03 | 2/6 | -4.80 | 0.74 |
| X4a COMEX momentum 13:00-13:30 NY | 4.84 | 0.93 | 2.82 | -1.89 | -4.31 | 0/6 | -4.70 | 1.00 |
| X4b COMEX momentum 12:30-13:30 NY | 4.84 | 0.88 | 2.80 | -1.93 | -2.96 | 1/6 | -4.73 | 1.00 |
| F1a WMR fix fade 16:05-16:35 | 4.97 | -0.09 | 1.00 | -1.09 | -4.94 | 0/6 | -2.08 | 1.00 |
| F1b WMR fix fade 16:05-17:30 | 4.97 | 0.25 | 1.02 | -0.78 | -2.29 | 0/6 | -1.80 | 1.00 |
| F2a pre-fix follow 15:30-16:00 | 4.98 | 0.05 | 0.96 | -0.91 | -2.90 | 1/6 | -1.87 | 1.00 |
| F3a short GBPUSD 08:00-12:00 London | 4.98 | 0.30 | 1.07 | -0.77 | -1.11 | 3/6 | -1.83 | 0.78 |
| F3b long GBPUSD 11:00-16:00 NY | 4.98 | 2.04 | 1.05 | +1.00 | 1.80 | 5/6 | -0.05 | 0.001 |
| F4a London-open momentum 15:00-16:00 | 4.97 | 0.98 | 1.11 | -0.13 | -0.31 | 1/6 | -1.23 | 0.30 |

F3b follow-up:
- A blind agent replicated DEV exactly.
- A post-hoc sealed test on 2017-01 to 2018-06 (n=370) gave gross +0.93 (p 0.21) and net -0.03. Dead.
- That sealed period is now spent for GBPUSD.

### Search 2: daily holds, set at 16:00 NY, swap charged

DEV: GBPUSD 2007-16, XAUUSD 2011-16. Figures are per day.

| Rule | Changes/wk | Gross | Cost | Swap | Net | t | Sharpe | Years + |
|---|---|---|---|---|---|---|---|---|
| D1 20d trend GBP | 0.52 | -1.39 | 0.13 | -0.37 | -1.88 | -1.52 | -0.48 | 3/10 |
| D2 60d trend GBP | 0.31 | 0.27 | 0.08 | -0.36 | -0.17 | -0.13 | -0.04 | 6/10 |
| D3 1d reversal GBP | 2.41 | -0.81 | 0.64 | -0.37 | -1.82 | -1.47 | -0.46 | 0/10 |
| D1 20d trend XAU | 0.45 | 0.73 | 0.26 | -0.56 | -0.08 | -0.03 | -0.01 | 2/6 |
| D2 60d trend XAU | 0.26 | 0.30 | 0.15 | -0.45 | -0.30 | -0.11 | -0.04 | 3/6 |
| D3 1d reversal XAU | 2.58 | -1.73 | 1.56 | -0.70 | -3.99 | -1.38 | -0.58 | 2/6 |

### Searches 3 and 5: Zarattini-Aziz-Barbon noise-area rule, published, VM 1, untuned

Per trade.

| Rule / period | Trades/wk | Gross | Cost | Net | t | Sharpe (1x) | Max DD (1x) | Years + |
|---|---|---|---|---|---|---|---|---|
| G-NA gold DEV 2011-16 | 3.87 | 3.34 | 2.74 | +0.60 | 0.45 | 0.19 | -7.3% | 4/6 |
| C-NA GBPUSD DEV 2007-16 | 5.71 | 0.58 | 1.24 | -0.65 | -1.54 | -0.49 | -28.3% | 2/10 |
| U-NA US500 DEV 2021-10 to 2024-12 | 4.82 | 4.18 | 1.10 | +3.08 | 1.91 | 1.08 | -5.0% | 4/4 |
| U-NA US500 HOLDOUT 2025-01 to 2026-10 | 4.68 | -0.23 | 0.76 | -0.99 | -0.51 | -0.38 | -11.3% | 1/2 |

Notes:
- Gold G-NA net at 2x cost: -1.66 bp/day. Gold holdout 2017-18 has not been run and is untouched.
- U-NA got a post-hoc one-shot holdout, because I did not state the minimum detectable effect beforehand. With 3.1 years, t = 2 needs Sharpe >= 1.13.
- U-NA was blind-replicated by a Haiku agent: DEV net 3.064, t 1.90; holdout net -0.986.
- External confirmation from NostroBenJ/intraday-strategy-replication: noise-area on ES had Sharpe 1.78 before publication and -0.19 after.

### Search 4: forums and literature (no backtests)

- "Verified" EAs: leveraged demo junk.
- Public forward tester: retired all 7 of his 2025 strategies.
- Broker data: 20.5% of retail CFD clients are profitable. Winners are dominated by XAUUSD latency arbitrage, which is banned at prop firms.

## 3. Cost table (verify before relying)

| Item | US500 | XAUUSD | GBPUSD |
|---|---|---|---|
| CFD round trip (measured, Dukascopy) | about 1.0 bp regular hours (0.51 pt median spread) | about 2.8 bp, wider at fixes | about 1.0-1.2 bp |
| CFD swap long / short per yr (OANDA EU) | -6.35% / +1.35% (Sep 2026) | -5.45% / +1.85% (Mar 2026) | -1.08% / -0.84% (Sep 2026) |
| FTMO Futures round trip (agent estimate) | MES about 0.7 bp | MGC about 0.6-0.7 bp | 6B about 1.2 bp; M6B 2+ bp |

FTMO CFD rules:
- Standard funded accounts must be flat through any break over 2 hours.
- Weekend holds require a Swing account.
- Evaluation phases are exempt from the holding rules.

FTMO Futures:
- Launched August 2026.
- Positions flattened at 16:10 ET; no swap.
- Monthly subscription.
- Commission $0.20 per side on micros, plus exchange fees.

## 4. Exact gold rule specs (for the next run)

Common to all three families:
- Prices are mid ((bid+ask)/2).
- "Price at local time T" = close of the 1-minute bar starting at T-1min, or the latest earlier bar if no more than 3 minutes stale. Otherwise the day is skipped.
- Fills: buys at ask, sells at bid, at the same bar.
- Weekdays only.
- Returns in bp of entry mid.

### A. Noise-area (G-NA)
- Session: COMEX day session, 08:20-13:30 America/New_York (length 310 min). Open = mid 'o' of the 08:20 bar.
- Checks at offsets 30, 60, ..., 300 min. Close at offset 310.
- sigma(T) = mean over the prior 14 VALID days of |price(T)/open - 1|. Use valid days only, not calendar days: this was a bug, now fixed.
- Bands:
  - Upper = max(open, prev close) × (1 + sigma)
  - Lower = min(open, prev close) × (1 - sigma)
  - VM = 1. Do not use 1.5.
- VWAP: volume-weighted mid since the session open. Old FX tick data has no volume, so it used tick count.
- Position logic at each check:
  - Flat: go long if p > Upper, short if p < Lower.
  - Long: reverse if p < Lower; otherwise exit if p < max(Upper, VWAP).
  - Short: reverse if p > Upper; otherwise exit if p > min(Lower, VWAP).
- Flat at session close.

### B. Fix fade (Europe/London time)
- X1a: signal = sign(P15:00 - P14:30). Trade the opposite direction from 15:05 to 15:35.
- X1b: same signal, trade 15:05 to 16:30.
- X2a: signal = sign(P10:30 - P10:00). Fade from 10:35 to 11:05.
- X2b: same signal, fade 10:35 to 12:00.

### C. COMEX momentum (America/New_York time)
- X4a: signal = sign(P08:50 - P08:20). Follow it from 13:00 to 13:30.
- X4b: same signal, follow 12:30 to 13:30.

### Planned run
- DEV: 2021-10 to 2024-12. HOLDOUT: 2025-01 to 2026-10, run once.
- Costs: MGC cost of about 0.65 bp round trip (stress 2x), alongside the actual CFD spread.
- DEV pass requires all of:
  - gross >= 1.4 bp/trade
  - net t >= 2, or the minimum detectable effect logged beforehand
  - net > 0 at 2x cost
  - >= 60% of years positive
- Holdout pass: net > 0, one-sided p < 0.10.
- Blind replication by Haiku, from the spec only.

## 5. Data formats

- Tick source: Dukascopy CSVs from GitHub FX-Data/FX-Data-{XAUUSD,GBPUSD,EURUSD}-DS. One branch per year: XAUUSD 2011-2018, GBPUSD 2007-2018 (2018 ends 06-19). Files are XAUUSD/YYYY/MM/YYYY-MM-DD--HHh_ticks.csv. Rows have no header: `YYYY.MM.DD HH:MM:SS.fff,bid,ask,bidvol,askvol`. Timestamps are UTC.
  - Gold prices in this mirror are scaled ÷100 (13.13 means $1,313). Returns and bp are unaffected.
- Rebuild the bars with `python3 scripts/build_bars.py SYMBOL YEAR [YEAR...]`. Output: data/{SYMBOL}_{YEAR}.pkl.
- Bar pickles: pandas DataFrame indexed by UTC timestamp, where the timestamp is the bar START minute. Columns: o, h, l, c (mid), bc, ac (bid/ask close), spr (mean spread), n (tick count, or volume for US500).
- US500 bars: data/US500_all.pkl. Same columns, with n = bid_volume_millions + ask_volume_millions. Built from the raw export below. Not in the tarball; rebuild it from the export (conversion code is in SEARCH_LOG and this file's section 6).
- Raw export format (US500, CSV gzip, header row): `timestamp_utc,bid_open,bid_high,bid_low,bid_close,bid_volume_millions,ask_open,ask_high,ask_low,ask_close,ask_volume_millions`. Timestamps are ISO with Z, bar start, 1-minute.
- Reachable from the sandbox: GitHub (git, raw) and PyPI only. Recent data has to come from Jake.

## 6. Scripts

- `build_bars.py`: streams FX-Data ticks into 1-min bars.
- `battery.py`: Search 1, 14 rules. Exports load(), at() and COMM. Run as `python3 battery.py dev|sealed`.
- `daily.py`: Search 2. Run as `python3 daily.py dev|holdout`.
- `noise_area.py`: noise-area rule. CFG covers G-NA, C-NA, U-NA. Run as `python3 noise_area.py dev|holdout [name]`.
- To add a symbol: put its bars at data/{SYM}_*.pkl, add COMM[SYM], and add CFG/PER entries.

US500 conversion: read the CSV, set mid = (bid+ask)/2 for o/h/l/c, bc = bid_close, ac = ask_close, spr = ask_close - bid_close, n = bid_vol + ask_vol, index = timestamp_utc. Save as data/US500_all.pkl.

## 7. Pending decisions

1. XAUUSD 1-min bid/ask export for 2021-10 to 2026-10, same Dukascopy format as US500. This blocks the only open path.
2. Verify MGC costs from CME fees and FTMO Futures pages. The figures above are agent estimates.
3. Is FTMO Futures acceptable to Jake? It has a monthly fee, is intraday only, and is a different platform from TradeLocker.
4. FTMO MT5 swap values for the CFD account type Jake will actually use. Only OANDA EU proxies are on file.
5. VWAP Reclaim daily return series. Needed for the correlation gate on any US500 survivor. Moot for now.
6. If gold fails, the honest options are: fewer, larger events (breaking the 4/week floor); a different asset class; or no systematic trading at this cost tier.
7. stage0_spec.md (month-end rebalancing) is superseded. It fails the 4/week floor at about 1 event per month.

## 8. Protocol (lessons kept)

- Before any result, log the rules, costs, partitions, pass bar, and minimum detectable Sharpe (about 2/sqrt(years)).
- Use published parameters only.
- Charge actual bid/ask, and stress at 2x cost.
- Run the holdout once. Log any exception before running it, and apply exceptions symmetrically.
- Check data coverage before trusting a result.
- Blind-replicate every near-miss.
- Log every failure.
- Agents: Haiku for mechanical work, Sonnet for research judgment. Never spawn agents just to look busy.
