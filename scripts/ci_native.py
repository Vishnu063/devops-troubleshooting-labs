"""Prove native graders fail before repair and pass afterwards in disposable CI."""
import argparse,json,subprocess,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import native

def command(*args,expected=0):
    result=subprocess.run(args,cwd=ROOT)
    if result.returncode!=expected:raise RuntimeError(f'{args} returned {result.returncode}, expected {expected}')

def main():
    p=argparse.ArgumentParser();p.add_argument('runtime',choices=['docker','kubernetes']);p.add_argument('--id');a=p.parse_args()
    ids=[a.id] if a.id else sorted(native.DOCKER if a.runtime=='docker' else native.K8S)
    allowed=native.DOCKER if a.runtime=='docker' else native.K8S
    if any(i not in allowed for i in ids):p.error('ID does not belong to this runtime')
    for i in ids:
        print(f'=== Case {i}: expect failure, repair, expect recovery ===',flush=True)
        try:
            command(sys.executable,'lab.py','up',i)
            if a.runtime=='docker':
                time.sleep(2)
                command(sys.executable,'lab.py','check',i,expected=1)
                target=ROOT/'.lab-state'/i/'compose.json'
                target.write_text((ROOT/'runnable'/i/'fixed.json').read_text())
                command(sys.executable,'lab.py','up',i)
                passed=False
                for attempt in range(15):
                    if native.check_docker(i):passed=True;break
                    time.sleep(1)
                if not passed:raise RuntimeError('Repaired Docker HTTP check did not recover')
            else:
                # The client must exist so a routing failure isn't just missing test tooling.
                subprocess.run(['kubectl','--context','kind-devops-labs','-n','devops-lab-'+i,'wait','--for=condition=Ready','pod/client','--timeout=120s'],check=True)
                command(sys.executable,'lab.py','check',i,expected=1)
                if i=='056':
                    native.kube(i,'delete','deployment','web')
                    native.kube(i,'delete','pvc','web-data','--wait=false')
                    # The unbound claim should delete promptly; surface a delayed deletion.
                    for attempt in range(15):
                        if native.kube(i,'get','pvc','web-data',capture=True,ok=False).returncode:break
                        time.sleep(1)
                native.kube(i,'apply','-f',str(ROOT/'runnable'/i/'fixed.json'))
                subprocess.run(['kubectl','--context','kind-devops-labs','-n','devops-lab-'+i,'rollout','status','deployment/web','--timeout=150s'],check=True,cwd=ROOT)
                passed=False
                for attempt in range(15):
                    if native.check_kube(i):passed=True;break
                    time.sleep(2)
                if not passed:raise RuntimeError('Repaired Kubernetes behavior did not recover')
                command(sys.executable,'lab.py','check',i)
            print(f'PASS {i}: failure and repaired behavior verified',flush=True)
        finally:
            command(sys.executable,'lab.py','down',i)
if __name__=='__main__':main()
