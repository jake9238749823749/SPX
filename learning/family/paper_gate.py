"""Paper gate: a hypothesis enters family F1 only if it passes ALL of these, decided on paper, before any data access.
Input: a JSON spec with fields: id, instrument, trades_per_week, gross_bp_2023plus (credible, or null), cost_bp_rt, ftmo_legal (bool), exact_params (bool), evidence_2023plus (bool).
Usage: python3 paper_gate.py registry.jsonl"""
import json, sys
FAIL = []
def gate(s):
    r = []
    if s['instrument'] not in {'US500', 'SPXUSD', 'MES', 'ES', 'XAUUSD', 'MGC', 'GC', 'GBPUSD', '6B', 'M6B'}: r.append('instrument')
    if not s.get('ftmo_legal'): r.append('ftmo_legal')
    if not s.get('exact_params'): r.append('unspecifiable')
    if s.get('trades_per_week', 0) < 4: r.append('frequency<4/wk')
    g, c = s.get('gross_bp_2023plus'), s.get('cost_bp_rt')
    if g is None or not s.get('evidence_2023plus'): r.append('no 2023+ gross evidence')
    elif c is None or g < 2 * c: r.append('gross<2x cost')
    return r
recs = [json.loads(l) for l in open(sys.argv[1])]
for s in recs:
    # registry entries don't carry gate fields; fill from known facts in the registry notes
    known = {
      'orb-mes-dev-holdout-spent': dict(trades_per_week=2.75, gross_bp_2023plus=-1.56, cost_bp_rt=0.7, evidence_2023plus=True, ftmo_legal=True, exact_params=True, instrument='MES'),
      'noise-area-us500-spent': dict(trades_per_week=4.7, gross_bp_2023plus=-0.23, cost_bp_rt=0.76, evidence_2023plus=True, ftmo_legal=True, exact_params=True, instrument='US500'),
      'gold-tsmom-12m': dict(trades_per_week=0.2, gross_bp_2023plus=-0.17, cost_bp_rt=0.65, evidence_2023plus=True, ftmo_legal=True, exact_params=True, instrument='XAUUSD'),
      'gold-breakout-ea-77691': dict(trades_per_week=0.6, gross_bp_2023plus=None, cost_bp_rt=2.8, evidence_2023plus=False, ftmo_legal=True, exact_params=True, instrument='XAUUSD'),
      'spy-intraday-momentum-zab': dict(trades_per_week=5, gross_bp_2023plus=None, cost_bp_rt=1.0, evidence_2023plus=False, ftmo_legal=True, exact_params=False, instrument='SPXUSD'),
      'pre-fomc-drift': dict(trades_per_week=0.15, gross_bp_2023plus=None, cost_bp_rt=0.7, evidence_2023plus=False, ftmo_legal=True, exact_params=True, instrument='ES'),
      'turn-of-month-equity': dict(trades_per_week=0.2, gross_bp_2023plus=None, cost_bp_rt=0.7, evidence_2023plus=False, ftmo_legal=True, exact_params=True, instrument='ES'),
    }
    f = {**s, **known.get(s['id'], {})}
    r = gate(f)
    print(f"{s['id']:32s} {'PASS' if not r else 'FAIL: '+', '.join(r)}")
