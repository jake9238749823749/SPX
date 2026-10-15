# Recursive improvement loop (goal: find a trading edge; target stated by Jake: millions in one year)

## Feasibility gate (run first, every cycle)
Required return = $1M ÷ capital.
| capital | required/yr | status |
|---|---|---|
| $50k | 2000% | impossible without ruin |
| $100k | 1000% | impossible without ruin |
| $1M | 100% | impossible without ruin |
| $10M | 10% | needs an edge like the best quant funds |
| $25M | 4% | index-like return on capital |
Plausible edge after costs for this program: about 0-1 Sharpe, roughly 0-10%/yr unlevered at 10% vol.
GATE: if required return > 2× plausible edge, the target is infeasible for that capital. Say so in JOURNAL.md and change the goal to what is achievable (growth of skill and capital), not a fantasy number.
Current verdict: $1M in one year is infeasible from the capital this repo assumes. The FTMO challenge is a fee-capped option, not a path to it.

## Cycle (one per session)
1. Read KNOWLEDGE.md and the last 3 JOURNAL entries.
2. Gate check above. Log the result.
3. Pick the single open question with the highest expected information per hour (currently: the calibration loop proposed to Jake; the fee check that decides the microstructure paper answer).
4. Pre-register a hypothesis in learning/ with its kill condition, BEFORE touching data.
5. Test only on data not yet used, or log it as forward. Any reused data is a post-hoc exception and must say so.
6. Score. Update KNOWLEDGE.md with a grade and a citation (file or commit).
7. Journal: learned, wrong, next question.
8. Commit and push.

## Stop conditions for the loop
- Gate fails for the target: the loop continues only on capital-growth and skill goals, not on the millions target.
- Three consecutive cycles without a new graded fact: stop and ask Jake for new information (fills, capital, a data source). Idling is not progress.
- Any action that publishes, trades real money, or enables a scheduled forecast requires Jake's explicit approval.
