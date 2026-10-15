# Audit queue (claims to audit, in priority order). Status: open / in progress / done
| # | Claim | Source | Why it matters | Status |
|---|---|---|---|---|
| 001 | ORB on US500, 50.9% win, PF 1.18 | TradingView fabledforman | Popular open-source rule | DONE: FAIL |
| 002 | Gold Breakout EA XAUUSD H4, +90% 2020-26, 198 trades | mql5.com/en/code/77691 | Open source, but 0.6 trades/week, all buys | open |
| 003 | Gold overnight hold (GLD 16:00 to 09:30) ~4 bp | quantifiedstrategies substack, 2026-03 | Fails instrument and FTMO rules; only checks the claim | open |
| 004 | Zarattini SPY intraday momentum, net Sharpe 1.33 | concretumgroup.com | Cited by many; noise-area family | open |
| 005 | Alpha Arena S1 results (LLM live trading) | forklog.com (secondhand) | Largest public AI-trading test | open, needs primary source |
| 006 | StockBench LLM results, Sonnet +2.2% | arxiv 2510.02209 | Claims post-cutoff | open |
| 007 | Monday Dip EA US500 D1 | mql5.com/en/code/78343 | Long-only D1, frequency fails | open |
| 008 | MES VWAP / "PF 8.00" TradingView script | TradingView | Vendor claim, likely no costs | open |

Rules: a claim is "unauditable" if rules can't be copied. Log every status change with a date in the row.
