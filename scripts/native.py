"""Local-only native lab lifecycle. Never creates cloud resources."""
import json
import shutil
import subprocess
import urllib.error
import urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
K8S={'023','024','025','026','027','050','051','052','056','057'}
DOCKER={'019','020','021'}
GIT={'013','040'}

def run(args,cwd=None,capture=False,timeout=45,ok=True):
    result=subprocess.run(args,cwd=cwd,text=True,stdout=subprocess.PIPE if capture else None,stderr=subprocess.PIPE if capture else None,timeout=timeout)
    if ok and result.returncode:
        raise RuntimeError((result.stderr or result.stdout or 'Command failed').strip())
    return result

def kube(i,*args,capture=False,ok=True):
    return run(['kubectl','--context','kind-devops-labs','--request-timeout=10s','-n','devops-lab-'+i,*args],capture=capture,ok=ok,timeout=25)

def compose(i,*args,capture=False,ok=True):
    return run(['docker','compose','-p','devopslab'+i,'-f',str(ROOT/'.lab-state'/i/'compose.json'),*args],capture=capture,ok=ok)

def git(path,*args,capture=False,ok=True):return run(['git','-C',str(path),*args],capture=capture,ok=ok)

def init_git(i,path):
    path.mkdir(parents=True)
    git(path,'init','-b','main')
    git(path,'config','user.name','Lab Engineer');git(path,'config','user.email','lab@example.test')
    def commit(content,message):
        (path/'app.conf').write_text(content);git(path,'add','app.conf');git(path,'commit','-m',message)
    commit('TIMEOUT=30\nRETRIES=3\n','Known working release')
    if i=='013':
        git(path,'checkout','-b','feature')
        commit('TIMEOUT=60\nRETRIES=3\n','Increase request timeout')
        git(path,'checkout','main')
        commit('TIMEOUT=30\nRETRIES=5\n','Increase transient retry budget')
        result=git(path,'merge','feature',ok=False)
        if result.returncode!=1:raise RuntimeError('Expected merge conflict was not created.')
    else:commit('TIMEOUT=0\nRETRIES=3\n','Faulty release removes timeout')

def check_git(i,path):
    if not (path/'.git').is_dir():raise RuntimeError('Run up first.')
    text=(path/'app.conf').read_text()
    clean=not git(path,'status','--porcelain',capture=True).stdout.strip()
    parents=git(path,'rev-list','--parents','-n','1','HEAD',capture=True).stdout.split()
    if i=='013':return clean and text=='TIMEOUT=60\nRETRIES=5\n' and len(parents)==3
    count=int(git(path,'rev-list','--count','HEAD',capture=True).stdout)
    return clean and text=='TIMEOUT=30\nRETRIES=3\n' and count>=3

def check_docker(i):
    cid=compose(i,'ps','--all','-q','web',capture=True).stdout.strip()
    if not cid:return False
    info=json.loads(run(['docker','inspect',cid],capture=True).stdout)[0]
    if not info['State']['Running']:return False
    bindings=[x for values in (info['NetworkSettings']['Ports'] or {}).values() if values for x in values]
    if not bindings:return False
    port=bindings[0]['HostPort']
    try:
        with urllib.request.urlopen(f'http://127.0.0.1:{port}/',timeout=3) as response:
            return response.status==200 and b'Welcome to nginx' in response.read()
    except (urllib.error.URLError,TimeoutError,ConnectionError):return False

def check_kube(i):
    result=kube(i,'get','deployment','web','-o','json',capture=True,ok=False)
    if result.returncode:return False
    d=json.loads(result.stdout);s=d.get('status',{})
    if s.get('observedGeneration',0)<d['metadata']['generation'] or s.get('updatedReplicas',0)!=1 or s.get('availableReplicas',0)!=1:return False
    if i=='023':
        result=kube(i,'exec','deployment/web','--','cat','/config/app.conf',capture=True,ok=False)
        return result.returncode==0 and 'mode=training' in result.stdout
    if i=='056':
        result=kube(i,'exec','deployment/web','--','sh','-c','echo lab-check > /data/check && test "$(cat /data/check)" = lab-check',capture=True,ok=False)
        if result.returncode:return False
    result=kube(i,'exec','client','--','wget','-qO-','-T','3','http://web/',capture=True,ok=False)
    return result.returncode==0 and ('Welcome to nginx' in result.stdout or (i=='050' and 'Directory listing' in result.stdout))

def operate(action,i):
    if i not in K8S|DOCKER|GIT:
        print('This case is an evidence drill. Use show, evidence, hint, and solution.');return 2
    work=ROOT/'.lab-state'/i
    try:
        if i in GIT:
            if not shutil.which('git'):raise RuntimeError('Git is required.')
            if action=='up':
                if not work.exists():init_git(i,work/'repo')
                print(f'Investigate and repair {work}/repo. Initial check should fail.');return 0
            if action=='check':passed=check_git(i,work/'repo')
            else:
                if work.exists():shutil.rmtree(work)
                print('Lab workspace removed.');return 0
        elif i in DOCKER:
            if not shutil.which('docker'):raise RuntimeError('Docker Engine and Docker Compose v2 are required.')
            if action=='up':
                work.mkdir(parents=True,exist_ok=True);(work/'empty').mkdir(exist_ok=True)
                target=work/'compose.json'
                if not target.exists():shutil.copyfile(ROOT/'runnable'/i/'broken.json',target)
                compose(i,'up','-d')
                print(f'Edit {target}, then rerun up. Initial check should fail.');return 0
            if not (work/'compose.json').exists():raise RuntimeError('Run up first.')
            if action=='check':passed=check_docker(i)
            else:
                compose(i,'down','--volumes','--remove-orphans');shutil.rmtree(work)
                print('Lab containers and workspace removed.');return 0
        else:
            if not shutil.which('kubectl'):raise RuntimeError('kubectl and the local kind-devops-labs context are required. See docs/LABS.md.')
            # Confirm the context is actually a local kind node, not a renamed cloud context.
            cluster=run(['kubectl','--context','kind-devops-labs','--request-timeout=10s','get','nodes','-o','json'],capture=True,timeout=20)
            nodes=json.loads(cluster.stdout).get('items',[])
            if not nodes or any(n['metadata'].get('labels',{}).get('kubernetes.io/hostname','').split('-control-plane')[0].split('-worker')[0]!='devops-labs' for n in nodes):
                raise RuntimeError('Expected nodes belonging to a local kind cluster named devops-labs.')
            if action=='up':
                ns={'apiVersion':'v1','kind':'Namespace','metadata':{'name':'devops-lab-'+i,'labels':{'devops-troubleshooting-labs':'true'}}}
                work.mkdir(parents=True,exist_ok=True);(work/'namespace.json').write_text(json.dumps(ns))
                kube(i,'apply','-f',str(work/'namespace.json'))
                kube(i,'apply','-f',str(ROOT/'runnable'/i/'broken.json'))
                print(f'Investigate namespace devops-lab-{i}. Initial check should fail.');return 0
            if action=='check':passed=check_kube(i)
            else:
                result=kube(i,'get','namespace','devops-lab-'+i,'-o','json',capture=True,ok=False)
                if result.returncode:
                    print('Namespace absent or unavailable; no deletion performed.');return 1
                if json.loads(result.stdout)['metadata'].get('labels',{}).get('devops-troubleshooting-labs')!='true':raise RuntimeError('Refusing to delete an unlabelled namespace.')
                kube(i,'delete','namespace','devops-lab-'+i,'--wait=false')
                if work.exists():shutil.rmtree(work)
                print('Lab namespace deletion requested. PVC data in this lab namespace is disposable.');return 0
        print('PASS: expected recovery checks succeeded.' if passed else 'FAIL: recovery criteria not met. Inspect the live evidence and retry.')
        return 0 if passed else 1
    except (RuntimeError,FileNotFoundError,subprocess.TimeoutExpired,json.JSONDecodeError) as error:
        print(f'Lab error: {error}');return 2
