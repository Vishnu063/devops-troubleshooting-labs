"""Reproducible local faults, scoped cleanup, and behavioral recovery grading."""
import json
import shutil
import subprocess
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from registry import RUNTIMES
ROOT=Path(__file__).resolve().parents[1]
K8S={i for i,r in RUNTIMES.items() if r=='kubernetes'}
DOCKER={i for i,r in RUNTIMES.items() if r=='docker'}
GIT={i for i,r in RUNTIMES.items() if r=='git'}

def run(args,cwd=None,capture=False,timeout=45,ok=True):
    r=subprocess.run(args,cwd=cwd,text=True,stdout=subprocess.PIPE if capture else None,stderr=subprocess.PIPE if capture else None,timeout=timeout)
    if ok and r.returncode:raise RuntimeError((r.stderr or r.stdout or 'Command failed').strip())
    return r

def kube(i,*args,capture=False,ok=True):
    return run(['kubectl','--context','kind-devops-labs','--request-timeout=10s','-n','devops-lab-'+i.lower(),*args],capture=capture,ok=ok,timeout=25)

def compose(i,*args,capture=False,ok=True):
    return run(['docker','compose','-p','devopslab'+i.lower(),'-f',str(ROOT/'.lab-state'/i/'compose.json'),*args],capture=capture,ok=ok,timeout=120)

def git(path,*args,capture=False,ok=True):return run(['git','-C',str(path),*args],capture=capture,ok=ok)

def init_git(i,path):
    path.mkdir(parents=True);git(path,'init','-b','main')
    git(path,'config','user.name','Lab Engineer');git(path,'config','user.email','lab@example.test')
    def commit(content,message):
        (path/'app.conf').write_text(content);git(path,'add','app.conf');git(path,'commit','-m',message)
    commit('TIMEOUT=30\nRETRIES=3\n','Known working release')
    if i=='013':
        git(path,'checkout','-b','feature');commit('TIMEOUT=60\nRETRIES=3\n','Increase request timeout')
        git(path,'checkout','main');commit('TIMEOUT=30\nRETRIES=5\n','Increase transient retry budget')
        if git(path,'merge','feature',ok=False).returncode!=1:raise RuntimeError('Expected merge conflict was not created.')
    else:commit('TIMEOUT=0\nRETRIES=3\n','Faulty release removes timeout')
    # Preserve the baseline release IDs so destructive history rewrites cannot pass.
    commits=git(path,'rev-list','--all',capture=True).stdout.splitlines()
    (path.parent/'baseline.json').write_text(json.dumps(commits))

def check_git(i,path):
    if not (path/'.git').is_dir():raise RuntimeError('Run up first.')
    baseline=json.loads((path.parent/'baseline.json').read_text())
    for commit in baseline:
        if git(path,'merge-base','--is-ancestor',commit,'HEAD',capture=True,ok=False).returncode:return False
    text=(path/'app.conf').read_text()
    clean=not git(path,'status','--porcelain',capture=True).stdout.strip()
    parents=git(path,'rev-list','--parents','-n','1','HEAD',capture=True).stdout.split()
    if i=='013':return clean and text=='TIMEOUT=60\nRETRIES=5\n' and len(parents)==3
    return clean and text=='TIMEOUT=30\nRETRIES=3\n' and int(git(path,'rev-list','--count','HEAD',capture=True).stdout)>len(baseline)

def docker_info(i):
    cid=compose(i,'ps','--all','-q','web',capture=True).stdout.strip()
    return json.loads(run(['docker','inspect',cid],capture=True).stdout)[0] if cid else None

def fetch(url):
    # Loopback/container lab requests must not go through a user's proxy configuration.
    with urllib.request.build_opener(urllib.request.ProxyHandler({})).open(url,timeout=3) as r:
        return r.status,r.read()

def check_docker(i):
    info=docker_info(i)
    if not info or not info['State']['Running']:return False
    ports=[x for values in (info['NetworkSettings']['Ports'] or {}).values() if values for x in values]
    if not ports or any(x['HostIp']!='127.0.0.1' for x in ports):return False
    base=f"http://127.0.0.1:{ports[0]['HostPort']}"
    try:
        if i=='033':
            for query in ['up{job="lab"}','lab_requests_total{job="lab"}']:
                status,body=fetch(base+'/api/v1/query?'+urllib.parse.urlencode({'query':query}))
                result=json.loads(body).get('data',{}).get('result',[])
                if status!=200 or not result or float(result[0]['value'][1])!=(1 if query.startswith('up') else 42):return False
            return True
        status,body=fetch(base+'/')
        expected={'005':b'permissions-recovered','006':b'Directory listing','010':b'Directory listing','049':b'database-roundtrip-ok'}.get(i,b'Welcome to nginx')
        return status==200 and expected in body
    except (urllib.error.URLError,TimeoutError,ConnectionError,ValueError):return False

def deployments_ready(i):
    for name in (['web','legacy'] if i=='081' else ['web']):
        r=kube(i,'get','deployment',name,'-o','json',capture=True,ok=False)
        if r.returncode:return False
        d=json.loads(r.stdout);s=d.get('status',{});desired=d['spec'].get('replicas',1)
        if desired<1 or s.get('observedGeneration',0)<d['metadata']['generation'] or s.get('updatedReplicas',0)!=desired or s.get('availableReplicas',0)!=desired:return False
    return True

def check_kube(i):
    if not deployments_ready(i):return False
    if i=='023':
        r=kube(i,'exec','deployment/web','--','cat','/config/app.conf',capture=True,ok=False)
        return r.returncode==0 and 'mode=training' in r.stdout
    if i=='054':
        r=kube(i,'exec','deployment/web','--','nslookup','kubernetes.default.svc.cluster.local',capture=True,ok=False)
        if r.returncode:return False
    if i=='056':
        r=kube(i,'exec','deployment/web','--','sh','-c','echo lab-check > /data/check && test "$(cat /data/check)" = lab-check',capture=True,ok=False)
        if r.returncode:return False
    if i=='081':
        r=kube(i,'get','endpointslices','-l','kubernetes.io/service-name=web','-o','json',capture=True)
        slices=json.loads(r.stdout)['items'];endpoints=[]
        for s in slices:
            for e in s.get('endpoints',[]):
                if e.get('conditions',{}).get('ready',True):
                    for address in e['addresses']:
                        for port in s['ports']:endpoints.append((address,port['port']))
        if len(endpoints)<2:return False
        for address,port in endpoints:
            r=kube(i,'exec','client','--','wget','-qO-','-T','3',f'http://{address}:{port}/',capture=True,ok=False)
            if r.returncode or 'Welcome to nginx' not in r.stdout:return False
    r=kube(i,'exec','client','--','wget','-qO-','-T','3','http://web/',capture=True,ok=False)
    return r.returncode==0 and (('Directory listing' if i in ['050','M03'] else 'Welcome to nginx') in r.stdout)

def stability_signature(i):
    if i in DOCKER:
        d=docker_info(i)
        return (d['Id'],d['State']['StartedAt'],d['RestartCount']) if d else None
    if i in K8S:
        result=kube(i,'get','pods','-o','json',capture=True)
        return sorted((p['metadata']['uid'],s['name'],s['restartCount']) for p in json.loads(result.stdout)['items'] for s in p.get('status',{}).get('containerStatuses',[]))
    return None

def grade(i,samples=3,interval=1):
    if i in GIT:return check_git(i,ROOT/'.lab-state'/i/'repo')
    before=stability_signature(i)
    for n in range(samples):
        if not (check_docker(i) if i in DOCKER else check_kube(i)):return False
        if n+1<samples:time.sleep(interval)
    return before is not None and before==stability_signature(i)

def guard_cluster():
    if not shutil.which('kubectl'):raise RuntimeError('kubectl and local kind-devops-labs context required. See docs/LABS.md.')
    result=run(['kubectl','--context','kind-devops-labs','--request-timeout=10s','get','nodes','-o','json'],capture=True,timeout=20)
    nodes=json.loads(result.stdout).get('items',[])
    if not nodes or any(not n['metadata']['name'].startswith('devops-labs-') or not n.get('spec',{}).get('providerID','').startswith('kind://') for n in nodes):raise RuntimeError('Only the dedicated local kind cluster devops-labs is supported.')

def owned_namespace(i):
    r=kube(i,'get','namespace','devops-lab-'+i.lower(),'--ignore-not-found','-o','json',capture=True)
    if not r.stdout.strip():return False
    if json.loads(r.stdout)['metadata'].get('labels',{}).get('devops-troubleshooting-labs')!='true':raise RuntimeError('Refusing to modify an unlabelled namespace.')
    return True

def operate(action,i,samples=3,interval=1):
    if i not in RUNTIMES:print('This case is an evidence drill. Use show, evidence, hint, and solution.');return 2
    work=ROOT/'.lab-state'/i
    try:
        if action=='reset':
            if operate('down',i):return 2
            if i in K8S:
                deadline=time.monotonic()+45
                while owned_namespace(i):
                    if time.monotonic()>deadline:raise RuntimeError('Namespace still terminating. Wait before retrying reset.')
                    time.sleep(1)
            return operate('up',i)
        if i in GIT:
            if not shutil.which('git'):raise RuntimeError('Git is required.')
            if action=='up':
                if not work.exists():init_git(i,work/'repo')
                print(f'Investigate {work}/repo. Initial check should fail.');return 0
            if action=='down':
                if work.exists():shutil.rmtree(work)
                print('Lab workspace removed.');return 0
        elif i in DOCKER:
            if not shutil.which('docker'):raise RuntimeError('Docker Engine and Compose v2 required.')
            if action=='up':
                work.mkdir(parents=True,exist_ok=True);(work/'empty').mkdir(exist_ok=True)
                source=ROOT/'runnable'/i
                if (source/'assets').exists():shutil.copytree(source/'assets',work/'assets',dirs_exist_ok=True) if not (work/'assets').exists() else None
                target=work/'compose.json'
                if not target.exists():shutil.copyfile(source/'broken.json',target)
                compose(i,'up','-d');print(f'Edit {target} or its assets, then rerun up. Initial check should fail.');return 0
            if action=='down':
                if (work/'compose.json').exists():compose(i,'down','--volumes','--remove-orphans')
                if work.exists():shutil.rmtree(work)
                print('Lab containers and workspace removed.');return 0
            if not (work/'compose.json').exists():raise RuntimeError('Run up first.')
        else:
            guard_cluster();exists=owned_namespace(i)
            if action=='up':
                work.mkdir(parents=True,exist_ok=True)
                ns={'apiVersion':'v1','kind':'Namespace','metadata':{'name':'devops-lab-'+i.lower(),'labels':{'devops-troubleshooting-labs':'true'}}}
                (work/'namespace.json').write_text(json.dumps(ns));kube(i,'apply','-f',str(work/'namespace.json'));kube(i,'apply','-f',str(ROOT/'runnable'/i/'broken.json'))
                print(f'Investigate namespace devops-lab-{i.lower()}. Initial check should fail.');return 0
            if action=='down':
                if exists:kube(i,'delete','namespace','devops-lab-'+i.lower(),'--wait=false')
                if work.exists():shutil.rmtree(work)
                print('Lab namespace deletion requested; lab data is disposable.');return 0
            if not exists:raise RuntimeError('Run up first.')
        passed=grade(i,samples,interval)
        print(f'PASS: recovery verified across {samples if i not in GIT else 1} checks.' if passed else 'FAIL: recovery or stability criteria not met. Inspect live evidence and retry.')
        return 0 if passed else 1
    except (RuntimeError,OSError,subprocess.TimeoutExpired,ValueError) as error:
        print(f'Lab error: {error}');return 2
