# Self-improving forecaster: binding rules (committed 2026-10-15, before any forecast)

## What it forecasts
Each US trading weekday at 10:16 ET, the system forecasts P = probability that today's ORB day on US500 nets > 0 at MES cost.
ORB rules are frozen in edge/scripts/orb.py.
- The forecast is made before the system knows whether the OR-width filter passes.
- Only days with a setup are scored.
- Inputs allowed: news, macro calendar, overnight/pre-market narrative, cross-asset context, MEMORY.md. NO intraday US500 prices from after 09:30.
- The training cutoff (June 2026) is before every forecast date, so there is no lookahead.

## Baseline (the forecaster must beat it)
Constant P0 = 0.7254: the share of 2021-10..2024-12 ORB setup days that netted > 0 at MES cost (335 days).

## Honesty mechanics
1. **Commit-before-outcome.** Each forecast is one JSON line in forecasts/YYYY-MM.jsonl, committed and pushed before 10:20 ET. The git commit time is the timestamp. A forecast committed after 10:20 ET is void.
2. **Frozen champion.** prompts/lead_vN.md is identified by its SHA-256 in VERSIONS.md. No edits; changes create a new version.
3. **Champion and challenger.** At most one challenger at a time. Both forecast the same days, blind to each other.
   - The challenger replaces the champion only if its Brier score beats the champion's with a one-sided paired bootstrap p < 0.05 over >= 40 common scored days.
   - Otherwise it is rejected and logged in REJECTED.md, and it is never retried in the same form.
4. **The critic proposes; it never decides.** The monthly critic reads scored results and proposes exactly ONE change: a MEMORY.md lesson or a prompt edit. The change enters only as a challenger.
5. **Memory needs evidence.** A lesson enters MEMORY.md only through a challenger that won.
6. **Separate scorer.** score.py is deterministic code, not an LLM. Outcomes come from HistData SPXUSD ticks.

## Verdicts (fixed now)
- **PASS:** after >= 120 scored setup days, the champion's Brier skill vs P0 is > 0 with bootstrap 95% CI excluding 0, AND a veto (skip when P < 0.5) improves net bp per day after 2x MES cost relative to taking every setup.
- **KILL:** at 120 scored days, the CI includes 0, OR the forecast standard deviation is < 0.03 (it is just echoing the base rate). Then AI judgment adds nothing to ORB here.
- A PASS licenses only 1 MES on paper. It is not live money.
