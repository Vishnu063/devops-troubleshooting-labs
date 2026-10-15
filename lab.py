#!/usr/bin/env python3
"""Dependency-free incident practice CLI. Python 3.10+."""
import argparse,json,random,sys
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'scripts'))
from registry import RUNTIMES,RUNNABLE,COMPOUNDS

def cases():return json.loads((ROOT/'data/incidents.json').read_text())
def all_cases():return cases()+COMPOUNDS

def select(value):
    try:
        ident=str(value).upper() if str(value).upper().startswith('M') else str(int(value)).zfill(3)
        return next(c for c in all_cases() if c['id']==ident)
    except (ValueError,StopIteration):raise SystemExit('Unknown case. Use 001–100 or M01–M03.')

def state_path():return ROOT/'.practice/attempts.json'

def attempts():
    p=state_path()
    if not p.exists():return []
    try:
        value=json.loads(p.read_text())
        if not isinstance(value,list) or any(not isinstance(r,dict) or not {'id','score','minutes','hints'}<=r.keys() for r in value):raise ValueError()
        return value
    except (ValueError,OSError):raise SystemExit('Cannot read practice history. Preserve .practice/attempts.json before repairing it.')

def save_attempts(value):
    p=state_path();p.parent.mkdir(parents=True,exist_ok=True)
    tmp=p.with_suffix('.tmp');tmp.write_text(json.dumps(value,indent=2)+'\n');tmp.replace(p)

def main(argv=None):
    p=argparse.ArgumentParser(description='100 incident drills + compound incidents. Diagnose first; prove recovery.')
    sub=p.add_subparsers(dest='command',required=True)
    for name in ['list','random']:
        q=sub.add_parser(name);q.add_argument('--level',type=int,choices=[1,2,3]);q.add_argument('--tool');q.add_argument('--runnable',action='store_true');q.add_argument('--compound',action='store_true')
    for name in ['show','evidence','solution','up','check','down','reset']:
        q=sub.add_parser(name);q.add_argument('id')
        if name=='check':q.add_argument('--samples',type=int,choices=range(1,11),default=3);q.add_argument('--interval',type=float,default=1)
    q=sub.add_parser('hint');q.add_argument('id');q.add_argument('--step',type=int,choices=[1,2,3],default=1)
    q=sub.add_parser('record');q.add_argument('id');q.add_argument('--score',type=int,choices=range(11),required=True);q.add_argument('--minutes',type=int,required=True);q.add_argument('--hints',type=int,choices=range(4),default=0)
    sub.add_parser('progress')
    session=sub.add_parser('session',help='Timed sessions, hidden symptoms, and optional level unlocking').add_subparsers(dest='session_command',required=True)
    q=session.add_parser('start');q.add_argument('id',nargs='?');q.add_argument('--hidden',action='store_true');q.add_argument('--level',type=int,choices=[1,2,3]);q.add_argument('--tool');q.add_argument('--runnable',action='store_true');q.add_argument('--compound',action='store_true');q.add_argument('--unlock',action='store_true');q.add_argument('--minutes',type=int)
    for name in ['status','evidence','solution','up','check','reset','down','abandon','path']:session.add_parser(name)
    q=session.add_parser('hint');q.add_argument('--step',type=int,choices=[1,2,3],default=1)
    q=session.add_parser('finish');q.add_argument('--score',type=int,choices=range(11),required=True)
    a=p.parse_args(argv)
    if a.command=='session':
        import sessions
        return sessions.handle(a,sys.modules[__name__])
    if a.command in ['list','random']:
        source=COMPOUNDS if a.compound else cases()
        found=[c for c in source if (not a.level or c['level']==a.level) and (not a.tool or a.tool.casefold() in (c['tool']+' '+c['title']).casefold()) and (not a.runnable or c['id'] in RUNTIMES)]
        if not found:print('No matching cases.');return 0
        if a.command=='random':found=[random.choice(found)]
        for c in found:print(f"{c['id']}  L{c['level']}  {c['title']}  [{RUNTIMES.get(c['id'],'evidence')}]")
        return 0
    if a.command=='progress':
        history=attempts();latest={r['id']:r for r in history};standard={c['id'] for c in cases()}
        print(f'{len(standard & latest.keys())}/100 cases attempted · {len(history)} attempts · self-assessed scores')
        print(f"Compound incidents attempted: {len(set(RUNTIMES)-standard & latest.keys())}; qualifying completions: {len({r['id'] for r in history if r.get('completed')})}")
        for level in [1,2,3]:
            ids={c['id'] for c in cases() if c['level']==level};print(f'Level {level}: {len(ids & latest.keys())}/{len(ids)} attempted')
        for r in history[-5:]:print(f"{r['id']}: {r['score']}/10 · {r['minutes']} min · {r['hints']} hints")
        return 0
    c=select(a.id);compound=c['id'].startswith('M')
    folder=ROOT/'runnable'/c['id'] if compound else ROOT/f"scenarios/level-{c['level']}/{c['id']}"
    if a.command in ['up','check','down','reset']:
        from native import operate
        interval=getattr(a,'interval',1)
        if not 0<=interval<=10:p.error('--interval must be between 0 and 10 seconds')
        return operate(a.command,c['id'],getattr(a,'samples',3),interval)
    if a.command=='record':
        if a.minutes<1:p.error('--minutes must be positive')
        history=attempts();history.append(dict(id=c['id'],score=a.score,minutes=a.minutes,hints=a.hints,time=datetime.now(timezone.utc).isoformat(),completed=False,native_verified=False))
        save_attempts(history);print('Self-assessed attempt recorded locally. Use timed sessions for level unlocking.');return 0
    if a.command=='hint':
        values=['Compare the symptom with declared configuration and recent changes.',c.get('checks','Inspect workload startup, scheduling, and the full request path.'),c.get('cause','There are two independent faults. Inspect the separate solution only after attempting both.')]
        print(values[a.step-1]);return 0
    name='README.md' if a.command=='show' else a.command+'.md'
    print((folder/name).read_text());return 0
if __name__=='__main__':
    try:sys.exit(main())
    except KeyboardInterrupt:sys.exit(130)
