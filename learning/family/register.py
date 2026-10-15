"""Lock a hypothesis before any data access. Appends one JSON line to registry.jsonl.
Usage: python3 register.py spec.json
A spec must contain: id, source, instrument, rule (exact parameters), horizon, kill (kill condition), forward_start (YYYY-MM-DD).
Refuses any spec whose forward_start is not after today's lock date, or whose id already exists."""
import datetime, hashlib, json, os, sys
REG = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'registry.jsonl')
spec = json.load(open(sys.argv[1]))
for k in ['id', 'source', 'instrument', 'rule', 'horizon', 'kill', 'forward_start']:
    assert k in spec, f'missing {k}'
today = datetime.date.today().isoformat()
assert spec['forward_start'] > today, 'forward_start must be after lock date (no look at data already seen)'
ids = {json.loads(l)['id'] for l in open(REG)} if os.path.exists(REG) else set()
assert spec['id'] not in ids, 'duplicate id'
canon = json.dumps({k: spec[k] for k in ['id', 'source', 'instrument', 'rule', 'horizon', 'kill', 'forward_start']}, sort_keys=True)
rec = {**spec, 'lock_date': today, 'spec_sha256': hashlib.sha256(canon.encode()).hexdigest(), 'status': 'open', 'spent_on_known_data': spec.get('spent_on_known_data', False)}
with open(REG, 'a') as f: f.write(json.dumps(rec) + '\n')
print('locked', spec['id'], rec['spec_sha256'][:16])
