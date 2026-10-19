"""Prove real faults, incomplete repairs, full recovery, reset, and scoped cleanup."""
import argparse,copy,json,subprocess,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import native

def cli(*args,expected=0):
    r=subprocess.run([sys.executable,'lab.py',*args],cwd=ROOT)
    if r.returncode!=expected:raise RuntimeError(f'{args}: exit {r.returncode}, expected {expected}')

def wait_until(predicate,seconds=90):
    deadline=time.monotonic()+seconds
    while time.monotonic()<deadline:
        if predicate():return
        time.sleep(2)
    raise RuntimeError('Timed out waiting for expected native behavior')

def fault_observed(i):
    return native.fault_observed(i)

def rollout(i):
    for name in (['web','legacy'] if i=='081' else ['web']):
        subprocess.run(['kubectl','--context','kind-devops-labs','-n','devops-lab-'+i.lower(),'rollout','status','deployment/'+name,'--timeout=150s'],check=True)

def repair(i):
    if i in native.DOCKER:
        (ROOT/'.lab-state'/i/'compose.json').write_text((ROOT/'runnable'/i/'fixed.json').read_text());cli('up',i)
    else:
        if i=='056':
            native.kube(i,'delete','deployment','web');native.kube(i,'delete','pvc','web-data','--wait=false')
            wait_until(lambda: not native.kube(i,'get','pvc','web-data','--ignore-not-found','-o','name',capture=True).stdout.strip(),45)
        native.kube(i,'apply','-f',str(ROOT/'runnable'/i/'fixed.json'));rollout(i)

def partial(i):
    data=json.loads((ROOT/'runnable'/i/'broken.json').read_text());fixed=json.loads((ROOT/'runnable'/i/'fixed.json').read_text())
    # Repair startup/scheduling only. The independent routing/readiness fault remains.
    data['items'][0]=copy.deepcopy(fixed['items'][0])
    if i=='M02':data['items'][0]['spec']['template']['spec']['containers'][0]['readinessProbe']=json.loads((ROOT/'runnable'/i/'broken.json').read_text())['items'][0]['spec']['template']['spec']['containers'][0]['readinessProbe']
    p=ROOT/'.lab-state'/i/'partial.json';p.write_text(json.dumps(data));native.kube(i,'apply','-f',str(p))
    if i!='M02':rollout(i)
    else:wait_until(lambda:'Readiness probe failed' in native.kube(i,'get','events','-o','json',capture=True).stdout)
    cli('check',i,expected=1)
    print(f'PASS {i}: incomplete repair still fails',flush=True)

def main():
    p=argparse.ArgumentParser();p.add_argument('runtime',choices=['docker','kubernetes']);p.add_argument('--id');a=p.parse_args()
    allowed=native.DOCKER if a.runtime=='docker' else native.K8S;ids=[a.id] if a.id else sorted(allowed)
    if any(i not in allowed for i in ids):p.error('ID does not belong to selected runtime')
    for i in ids:
        print(f'=== Case {i}: fault, repair, stability, reset ===',flush=True)
        try:
            cli('up',i)
            if i in native.K8S:
                subprocess.run(['kubectl','--context','kind-devops-labs','-n','devops-lab-'+i.lower(),'wait','--for=condition=Ready','pod/client','--timeout=120s'],check=True)
            wait_until(lambda:fault_observed(i),120)
            cli('check',i,expected=1)
            if i.startswith('M'):partial(i)
            repair(i);wait_until(lambda:native.grade(i,samples=3,interval=1),90);cli('check',i)
            # Exercise the public reset command after an actually repaired lab.
            cli('reset',i)
            if i in native.K8S:
                subprocess.run(['kubectl','--context','kind-devops-labs','-n','devops-lab-'+i.lower(),'wait','--for=condition=Ready','pod/client','--timeout=120s'],check=True)
            wait_until(lambda:fault_observed(i),120);cli('check',i,expected=1)
            print(f'PASS {i}: fault, repaired behavior, stability, and reset verified',flush=True)
        except Exception:
            if i in native.DOCKER:
                native.compose(i,'ps','--all',ok=False);native.compose(i,'logs','--tail','100',ok=False)
            else:
                native.kube(i,'get','pods','-o','wide',ok=False);native.kube(i,'get','events','--sort-by=.metadata.creationTimestamp',ok=False)
            raise
        finally:cli('down',i)
if __name__=='__main__':main()
