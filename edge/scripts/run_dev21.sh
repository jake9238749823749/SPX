#!/bin/sh
# Coverage check, then the DEV 2021-10..2024-12 gold run (prereg). One shot.
cd /home/user/SPX/edge/scripts
python3 -c "
import sys; sys.path.insert(0,'.'); from battery import load
b=load('XAUUSD_HD'); l=b.index.tz_convert('America/New_York')
s=b[(l.hour*60+l.minute>=500)&(l.hour*60+l.minute<810)&(l.weekday<5)]
d=s.groupby(s.index.tz_convert('America/New_York').strftime('%Y-%m')).apply(lambda x: x.index.tz_convert('America/New_York').date).apply(lambda x: len(set(x)))
print('COVERAGE session days/month:', d.to_dict()); print('months', len(d), 'min', d.min())"
for m in cfd mgc; do python3 noise_area.py dev21 $m G-NA21; python3 battery.py dev21 $m X1a X1b X2a X2b X4a X4b; done
