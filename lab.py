#!/usr/bin/env python3
"""Dependency-free practice CLI. Run from any working directory."""
import argparse
import json
import random
import sys
from datetime import datetime, timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'scripts'))
from build_docs import RUNNABLE

def cases():
    return json.loads((ROOT/'data/incidents.json').read_text())

def select(value):
    try:
        return next(c for c in cases() if c['id']==str(int(value)).zfill(3))
    except (ValueError,StopIteration):
        raise SystemExit('Unknown case. Use an ID from 001 to 100.')

def state_path():
    return ROOT/'.practice/attempts.json'

def attempts():
    p=state_path()
    if not p.exists():return []
    try:
        value=json.loads(p.read_text())
        if not isinstance(value,list):raise ValueError()
        return value
    except (ValueError,OSError):
        raise SystemExit('Cannot read practice history. Preserve .practice/attempts.json before repairing it.')

def main(argv=None):
    p=argparse.ArgumentParser(description='100 incident drills. Easy to start; diagnosis is your job.')
    sub=p.add_subparsers(dest='command',required=True)
    for name in ['list','random']:
        q=sub.add_parser(name);q.add_argument('--level',type=int,choices=[1,2,3]);q.add_argument('--tool');q.add_argument('--runnable',action='store_true')
    for name in ['show','evidence','solution','up','check','down']:
        q=sub.add_parser(name);q.add_argument('id')
    q=sub.add_parser('hint');q.add_argument('id');q.add_argument('--step',type=int,choices=[1,2,3],default=1)
    q=sub.add_parser('record');q.add_argument('id');q.add_argument('--score',type=int,choices=range(11),required=True);q.add_argument('--minutes',type=int,required=True);q.add_argument('--hints',type=int,choices=range(4),default=0)
    sub.add_parser('progress')
    a=p.parse_args(argv)
    if a.command in ['list','random']:
        found=[c for c in cases() if (not a.level or c['level']==a.level) and (not a.tool or a.tool.casefold() in (c['tool']+' '+c['title']).casefold()) and (not a.runnable or c['id'] in RUNNABLE)]
        if not found:print('No matching cases.');return 0
        if a.command=='random':found=[random.choice(found)]
        for c in found:print(f"{c['id']}  L{c['level']}  {c['title']}  [{'runnable' if c['id'] in RUNNABLE else 'evidence'}]")
        return 0
    if a.command=='progress':
        history=attempts();latest={r['id']:r for r in history}
        print(f'{len(latest)}/100 cases attempted · {len(history)} attempts · self-assessed scores')
        for level in [1,2,3]:
            ids={c['id'] for c in cases() if c['level']==level}
            print(f"Level {level}: {len(ids & latest.keys())}/{len(ids)} attempted")
        for r in history[-5:]:print(f"{r['id']}: {r['score']}/10 · {r['minutes']} min · {r['hints']} hints")
        return 0
    c=select(a.id)
    folder=ROOT/f"scenarios/level-{c['level']}/{c['id']}"
    if a.command in ['up','check','down']:
        from native import operate
        return operate(a.command,c['id'])
    if a.command=='record':
        if a.minutes<1:p.error('--minutes must be positive')
        history=attempts();history.append(dict(id=c['id'],score=a.score,minutes=a.minutes,hints=a.hints,time=datetime.now(timezone.utc).isoformat()))
        target=state_path();target.parent.mkdir(exist_ok=True)
        temporary=target.with_suffix('.tmp');temporary.write_text(json.dumps(history,indent=2)+'\n');temporary.replace(target)
        print('Attempt recorded locally. Scores are self-assessed.');return 0
    if a.command=='hint':
        values=['Compare the symptom with declared configuration and recent changes.',c['checks'],c['cause']]
        print(values[a.step-1]);return 0
    path=folder/('README.md' if a.command=='show' else a.command+'.md')
    print(path.read_text());return 0
if __name__=='__main__':
    try:sys.exit(main())
    except KeyboardInterrupt:sys.exit(130)
