# T1 pre-registration: 10-month moving-average timing vs buy-and-hold, S&P 500 (logged 2026-10-16, before any result)

## Hypothesis
Faber (2007) timing: hold the S&P 500 when its monthly price is above its 10-month simple moving average, otherwise hold cash. Published parameter (10 months), not tuned.
Question for the Robinhood goal: does it beat simply holding the index?

## Data
datasets/s-and-p-500 on GitHub (Shiller monthly data), fetched 2026-10-16.
- Prices are MONTHLY AVERAGES, not month-end closes. To avoid overlap bias, the signal from month t's average applies to the return from month t+1 to month t+2 (one extra month of lag). This is conservative.
- Dividends missing from 2023-07: carry forward the last known dividend yield (D/P).
- Interest rate: only a 10-year rate exists, missing from 2023-07. Cash is bracketed: LOWER bound cash = 0%; UPPER bound cash = 10-year rate / 12 (carried forward). The true T-bill rate lies between for most of the window.

## Windows
- TEST (out of sample, after the rule's publication): 2007-01 to 2026-09.
- Reference only (Faber's era, not a test): 1901-01 to 2006-12.

## Costs and taxes
- 2 bp per switch (ETF spread, $0 commission on Robinhood).
- Taxes not modelled numerically. Report the number of exits; each exit can realise a taxable gain, which favours buy-and-hold.

## Pass bar (TEST window, LOWER-bound cash)
Timing beats buy-and-hold if BOTH: (a) its Sharpe ratio is higher, with a 12-month block-bootstrap one-sided p < 0.10; and (b) its total return is no more than 1%/yr below buy-and-hold.
Otherwise FAIL, and buy-and-hold remains the benchmark to beat.
Reported either way: CAGR, volatility, Sharpe, max drawdown, months invested, exits, for both bounds.
