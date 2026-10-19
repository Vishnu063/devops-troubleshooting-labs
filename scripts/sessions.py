"""Timed, optional-gated practice sessions; progress stays on the learner's machine."""
import contextlib
import io
import json
import math
import random
import time
from datetime import datetime,timezone
from pathlib import Path
from registry import RUNTIMES,SYMPTOMS
ROOT=Path(__file__).resolve().parents[1]

def path():return ROOT/'.practice/session.json'

def write(value):
    p=path();p.parent.mkdir(parents=True,exist_ok=True)
    temporary=p.with_suffix('.tmp');temporary.write_text(json.dumps(value,indent=2)+'\n');temporary.replace(p)

def current(required=True):
    if not path().exists():
        if required:raise SystemExit('No active session. Run: python3 lab.py session start --hidden --runnable')
        return None
    try:
        value=json.loads(path().read_text())
        if not isinstance(value,dict) or not {'id','started','budget','hidden','hints','revealed','verified'}<=value.keys():raise ValueError()
        return value
    except (ValueError,OSError):raise SystemExit('Cannot read session history. Preserve .practice/session.json before repairing it.')

def unlocked(level,history,all_cases):
    if level==1:return True
    previous={c['id'] for c in all_cases if c['level']==level-1}
    completed={r['id'] for r in history if r.get('completed') and r.get('id') in previous}
    return len(completed)>=3

def status(s,c):
    elapsed=max(0,time.time()-s['started']);remaining=max(0,s['budget']-elapsed)
    print(f"{'Hidden incident' if s['hidden'] else c['id']+' · '+c['title']} · Level {c['level']}")
    print(f"Elapsed {int(elapsed)//60:02}:{int(elapsed)%60:02} · Remaining {int(remaining)//60:02}:{int(remaining)%60:02}"+(' · TIME EXPIRED' if elapsed>s['budget'] else ''))
    print(SYMPTOMS.get(c['id'],f"An incident affects the {c['tool']} environment. Investigate the supplied observations and restore the intended behavior."))
    print(f"Practice: {RUNTIMES.get(c['id'],'supplied evidence')} · Hints opened: {len(s['hints'])} · Solution revealed: {s['revealed']}")
    if c['id'] in RUNTIMES:print('Starting fault: '+('confirmed for this attempt' if s.get('fault_verified') else 'not confirmed — run session up or session verify-fault'))
    print('Use: session up | verify-fault | evidence | hint | check | status | finish | abandon')

def native_action(action,s,wait=120):
    import native
    # Resource paths and kubectl output necessarily identify local lab resources.
    # Suppress setup chatter in hidden mode, but print the workspace required to investigate.
    if s['hidden'] and action in ['up','reset']:
        out=io.StringIO()
        previous=native.QUIET
        try:
            native.QUIET=True
            with contextlib.redirect_stdout(out):result=native.operate(action,s['id'],wait=wait)
        finally:native.QUIET=previous
        if result:print(out.getvalue())
        else:
            runtime=RUNTIMES[s['id']]
            print('Investigate '+('namespace devops-lab-'+s['id'].lower()+' in context kind-devops-labs' if runtime=='kubernetes' else str(ROOT/'.lab-state'/s['id'])))
        return result
    return native.operate(action,s['id'],wait=wait)

def handle(args,api):
    action=args.session_command
    if action=='start':
        if current(False):raise SystemExit('A session is already active. Finish or abandon it before starting another.')
        all_cases=api.all_cases();level=args.level or (3 if args.compound else 1)
        if args.unlock and not unlocked(level,api.attempts(),all_cases):raise SystemExit(f'Level {level} locked: complete three distinct Level {level-1} sessions first (score >=7, within timer, no solution, at most one hint; native labs must pass). Omit --unlock for free practice.')
        choices=[c for c in all_cases if c['level']==level and (not args.runnable or c['id'] in RUNTIMES) and (not args.compound or c['id'].startswith('M')) and (not args.tool or args.tool.casefold() in c['tool'].casefold())]
        if args.id:
            candidate=api.select(args.id)
            if args.level and candidate['level']!=args.level:raise SystemExit('Selected case does not match --level.')
            if args.runnable and candidate['id'] not in RUNTIMES:raise SystemExit('Selected case is not runnable.')
            if args.compound and not candidate['id'].startswith('M'):raise SystemExit('Selected case is not compound.')
            if args.unlock and not unlocked(candidate['level'],api.attempts(),all_cases):raise SystemExit('Selected case level is locked.')
            choices=[candidate]
        if not choices:raise SystemExit('No matching cases.')
        c=random.choice(choices)
        minutes=c['minutes'] if args.minutes is None else args.minutes
        if minutes<1:raise SystemExit('--minutes must be positive.')
        s={'id':c['id'],'started':time.time(),'budget':minutes*60,'hidden':args.hidden,'hints':[],'revealed':False,'verified':False,'fault_verified':False}
        write(s);status(s,c);return 0
    if action=='path':
        history=api.attempts();all_cases=api.all_cases()
        for level in [1,2,3]:print(f"Level {level}: {'unlocked' if unlocked(level,history,all_cases) else 'locked — complete three distinct previous-level sessions'}")
        return 0
    s=current();c=api.select(s['id'])
    if action=='status':status(s,c);return 0
    if action=='abandon':path().unlink();print(f"Session abandoned. Clean up with: python3 lab.py down {s['id']}");return 0
    if action in ['up','check','reset','down','verify-fault']:
        if c['id'] not in RUNTIMES:print('Evidence-only session: explain your diagnosis, recovery, and verification in an incident report.');return 2
        if action in ['up','reset','down']:s['verified']=False;s['fault_verified']=False
        result=native_action(action,s,getattr(args,'wait',120))
        if action=='check':s['verified']=result==0
        if action in ['up','reset','verify-fault']:
            import native
            marker=native.ROOT/'.lab-state'/s['id']/'startup.json'
            if result==0 and marker.exists():
                proof=json.loads(marker.read_text())
                s['fault_verified']=proof.get('observed') is True and proof.get('checked_at',0)>=s['started']
            else:s['fault_verified']=False
            print('Starting fault confirmed for this attempt.' if s['fault_verified'] else 'Starting fault is not confirmed for this attempt. Use session verify-fault, or session reset to recreate it.')
        write(s);return result
    if action=='evidence':
        print('Synthetic investigation snapshot:')
        print(c.get('evidence',c.get('symptom','Collect live events, logs, workload state, and end-to-end requests.')))
        if c['id'].startswith('M'):print('Collect live Kubernetes evidence. There may be more than one fault.')
        return 0
    if action=='hint':
        step=args.step or next((n for n in [1,2,3] if n not in s['hints']),3)
        if step not in s['hints']:s['hints'].append(step)
        if step==3 and not c['id'].startswith('M'):s['revealed']=True
        write(s)
        if c['id'].startswith('M'):
            hints=['Check workload startup, scheduling, readiness, and the request path independently.','Inspect pod events, resources, probes, Service selectors, and EndpointSlices.','Each compound includes two independent faults. The separate solution identifies them.']
        else:hints=['Separate the failing dependency from the user-visible symptom.',c['checks'],c['cause']]
        print(f'Hint {step}/3'+(' · diagnosis revealed (practice only)' if step==3 and not c['id'].startswith('M') else ''))
        print(hints[step-1]);return 0
    if action=='solution':
        s['revealed']=True;write(s)
        solution=ROOT/'runnable'/c['id']/'solution.md' if c['id'].startswith('M') else ROOT/f"scenarios/level-{c['level']}/{c['id']}/solution.md"
        print(solution.read_text());return 0
    if action=='finish':
        native=c['id'] in RUNTIMES
        if native:
            result=native_action('check',s)
            if result:print('Recovery has not passed. Keep practicing or abandon the session.');return result
            if not s.get('fault_verified'):
                print('Recovery passes, but this attempt has no verified starting fault. Reset and reproduce the fault before claiming a completion.');return 2
        elapsed=max(0,time.time()-s['started'])
        completed=args.score>=7 and elapsed<=s['budget'] and not s['revealed'] and len(s['hints'])<=1
        entry={'id':c['id'],'score':args.score,'minutes':max(1,math.ceil(elapsed/60)),'seconds':round(elapsed),'hints':len(s['hints']),'time':datetime.now(timezone.utc).isoformat(),'completed':completed,'native_verified':native,'startup_verified':s.get('fault_verified',False),'solution_revealed':s['revealed'],'timed_out':elapsed>s['budget'],'mode':'hidden' if s['hidden'] else 'guided'}
        history=api.attempts();history.append(entry);api.save_attempts(history);path().unlink()
        print(f"Session recorded: {args.score}/10 self-assessed · {'counts toward level unlocking' if completed else 'practice attempt; does not count toward unlocking'}. Native recovery {'verified' if native else 'not applicable (evidence drill)'}. Clean up with: python3 lab.py down {c['id']}.")
        return 0
    raise SystemExit('Unknown session action.')

