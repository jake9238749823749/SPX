# Goal (changed 2026-10-16): grow a Robinhood account

Replaces the FTMO funded-account goal. Approved by Jake.

## What changes
| Item | FTMO (old) | Robinhood (new) |
|---|---|---|
| Account | Prop-firm challenge, fee per attempt | Your own money, Robinhood agentic account (separate MCP account) |
| Holding | Futures flat by 16:10 ET; CFD swap and weekend rules | Overnight and long holds allowed |
| Drawdown rule | $2,000 trailing (4%) ends the account | None imposed; risk limits are ours to set |
| Instruments | US500, XAUUSD, GBPUSD, CME micros | US stocks and ETFs (agentic account supports equities at launch, per third-party guides; unverified with Robinhood) |
| Costs | Spread + commission + swap | $0 commission; cost is the bid/ask spread and price improvement; no financing on cash positions; taxes on gains |
| Frequency floor | 4 trades/week | Dropped. It came from the FTMO framing; long holds now cost almost nothing per day |

## What carries over from the old program
- Intraday public rules on index and gold: no edge after costs (34 tests, edge/SEARCH_LOG.md). Still true on Robinhood: the cost per trade is still the spread.
- Decay of published intraday rules, and the protocol (pre-registration, one holdout, blind replication).
- The return arithmetic: plausible edge is about 0-10%/yr; leverage multiplies drawdowns.

## What opens up
- Long-horizon risk premia (broad index ETFs, diversified trend across ETFs) become viable, because holding costs are near zero and there is no daily flat rule.
- The benchmark every strategy must beat: buy-and-hold of a broad index ETF, after taxes.

## Standing rules (unchanged)
- No order placed through the Robinhood connector without Jake's per-order approval.
- Any strategy needs a pre-registration before data, and a forward test before money.
- Real-money size only after a pass, and never more than Jake states he can lose.
