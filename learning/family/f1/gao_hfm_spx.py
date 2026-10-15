"""LOCKED RULE (Gao, Han, Li, Zhou 2018, JFE: first half-hour return predicts last half-hour).
Per trading day, SPX index (SPXUSD HistData mid, New York time):
  r_first = close(10:00 bar) / open(09:30 bar) - 1
  if r_first > 0: buy at ask of the 15:30 bar, sell at bid of the 16:00 bar; if r_first < 0: the reverse. Else no trade.
Gross = direction * (mid_exit / mid_entry - 1) in bp. Cost: MES flat 0.70 bp round trip (1x) and 1.40 bp (2x), plus the bid/ask half-spread crossing charged on entry and exit.
Window W: 2018-07-01 to 2021-09-30 (unspent SPX window, see DATA_LEDGER.md).
"""
