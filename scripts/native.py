"""Reproducible local faults, scoped cleanup, and behavioral recovery grading."""
import json
import re
import shutil
import subprocess
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from registry import RUNTIMES
ROOT=Path(__file__).resolve().parents[1]
QUIET=False
K8S={i for i,r in RUNTIMES.items() if r=='kubernetes'}
DOCKER={i for i,r in RUNTIMES.items() if r=='docker'}
GIT={i for i,r in RUNTIMES.items() if r=='git'}

def run(args,cwd=None,capture=False,timeout=45,ok=True):
    capture=capture or QUIET
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
            for query in ['up{job="lab",instance="metrics:9100"}','lab_requests_total{job="lab",instance="metrics:9100"}']:
                status,body=fetch(base+'/api/v1/query?'+urllib.parse.urlencode({'query':query}))
                result=json.loads(body).get('data',{}).get('result',[])
                if status!=200 or len(result)!=1 or float(result[0]['value'][1])!=(1 if query.startswith('up') else 42):return False
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

def fault_observed(i):
    """Match live fault signals, not simply the inverse of the recovery grader."""
    if i in GIT:
        path=ROOT/'.lab-state'/i/'repo'
        if not (path/'.git').exists():return False
        if i=='013':
            return bool(git(path,'ls-files','--unmerged',capture=True).stdout.strip()) and '<<<<<<<' in (path/'app.conf').read_text()
        return (path/'app.conf').read_text()=='TIMEOUT=0\nRETRIES=3\n' and not git(path,'status','--porcelain',capture=True).stdout.strip()
    if i in DOCKER:
        d=docker_info(i)
        if not d:return False
        if i in ['006','019']:
            if d['State']['Status']!='exited' or d['State']['ExitCode']==0:return False
            logs=compose(i,'logs','--no-color','web',capture=True).stdout
            return bool(re.search(r'\bAddress (?:already )?in use\b',logs)) if i=='006' else 'required variable APP_MODE missing' in logs
        if not d['State']['Running']:return False
        ports=[(key,entry) for key,values in (d['NetworkSettings']['Ports'] or {}).items() for entry in (values or [])]
        if len(ports)!=1 or ports[0][1]['HostIp']!='127.0.0.1':return False
        target,port=ports[0];base=f"http://127.0.0.1:{port['HostPort']}"
        if i in ['010','020']:
            # Prove the process serves inside its container before treating the
            # failed published request as the intended networking fault.
            internal=compose(i,'exec','-T','web',*(['python','-c',"import urllib.request; assert urllib.request.urlopen('http://127.0.0.1:8080').status==200"] if i=='010' else ['wget','-qO-','http://127.0.0.1:80/']),capture=True,ok=False)
            configured=('127.0.0.1' in d['Config']['Cmd'] if i=='010' else target=='8080/tcp')
            return internal.returncode==0 and configured and not check_docker(i)
        try:
            if i=='033':
                _,body=fetch(base+'/api/v1/query?'+urllib.parse.urlencode({'query':'up{job="lab"}'}))
                values=json.loads(body)['data']['result']
                wrong_target=any(v['metric'].get('instance')=='metrics:9091' and float(v['value'][1])==0 for v in values)
                if not wrong_target:return False
                healthy=compose(i,'exec','-T','metrics','python','-c',"import urllib.request; assert b'lab_requests_total 42' in urllib.request.urlopen('http://127.0.0.1:9100/metrics').read()",capture=True,ok=False)
                return healthy.returncode==0
            status,body=fetch(base+'/')
        except urllib.error.HTTPError as error:
            status,body=error.code,error.read()
        except (urllib.error.URLError,TimeoutError,ConnectionError):return False
        if i=='005':return status==503 and b'Permission denied reading application data' in body
        if i=='012':
            healthy=compose(i,'exec','-T','backend','wget','-qO-','http://127.0.0.1:80/',capture=True,ok=False)
            return status==502 and b'Bad Gateway' in body and healthy.returncode==0 and 'Welcome to nginx' in healthy.stdout
        if i=='021':
            empty=ROOT/'.lab-state'/i/'empty'
            mounted=any(m.get('Destination')=='/usr/share/nginx/html' and Path(m.get('Source','')).resolve()==empty.resolve() for m in d.get('Mounts',[]))
            return status==403 and b'Forbidden' in body and mounted and empty.is_dir() and not any(empty.iterdir())
        if i=='049':
            ping=compose(i,'exec','-T','database','redis-cli','ping',capture=True,ok=False)
            return status==503 and b'Connection refused' in body and 'DB_HOST=localhost' in d['Config'].get('Env',[]) and ping.returncode==0 and 'PONG' in ping.stdout
        return False
    pods=json.loads(kube(i,'get','pods','-o','json',capture=True).stdout)['items']
    # A working investigation pod distinguishes lab faults from failed image
    # downloads or a broken client environment.
    if not any(p['metadata']['name']=='client' and any(c.get('type')=='Ready' and c.get('status')=='True' for c in p.get('status',{}).get('conditions',[])) for p in pods):return False
    workload=[p for p in pods if p['metadata']['name']!='client']
    observed=json.dumps([p.get('status',{}) for p in workload])
    events=json.loads(kube(i,'get','events','-o','json',capture=True).stdout)['items']
    messages=' '.join(e.get('message','') for e in events)
    if i in ['M01','M03']:
        service=json.loads(kube(i,'get','service','web','-o','json',capture=True).stdout)
        if service['spec'].get('selector')!={'app':'checkout'}:return False
    if i=='M02':
        deployment=json.loads(kube(i,'get','deployment','web','-o','json',capture=True).stdout)
        if deployment['spec']['template']['spec']['containers'][0].get('readinessProbe',{}).get('httpGet',{}).get('path')!='/not-ready':return False
    if i=='023':
        logs=kube(i,'logs','deployment/web','--tail=20',capture=True,ok=False)
        return 'app.conf' in logs.stdout and 'No such file' in logs.stdout
    if i in ['024','M01']:
        return ('ErrImagePull' in observed or 'ImagePullBackOff' in observed) and 'does-not-exist-lab' in messages and any(word in messages.lower() for word in ['not found','manifest unknown'])
    if i in ['025','M02']:return 'Insufficient cpu' in messages
    if i=='026':return 'CreateContainerConfigError' in observed and 'payment-config' in observed and 'not found' in observed
    if i in ['050','M03']:return 'OOMKilled' in observed
    if i=='051':return 'Readiness probe failed' in messages and '404' in messages
    if i=='052':return 'Liveness probe failed' in messages and any(s.get('restartCount',0)>0 for p in workload for s in p.get('status',{}).get('containerStatuses',[]))
    if i=='056':return 'fast-ssd' in messages and 'not found' in messages
    if i=='057':
        d=json.loads(kube(i,'get','deployment','web','-o','json',capture=True).stdout)
        return 'does-not-exist-lab' in messages and any(word in messages.lower() for word in ['not found','manifest unknown']) and any(c.get('reason')=='ProgressDeadlineExceeded' for c in d.get('status',{}).get('conditions',[]))
    if i=='080':return 'exceeded quota' in messages and 'best-effort-budget' in messages
    if i in ['027','054','081']:
        if not deployments_ready(i):return False
        if i=='027':
            service=json.loads(kube(i,'get','service','web','-o','json',capture=True).stdout)
            configured=service['spec'].get('selector')=={'app':'checkout'}
        else:
            d=json.loads(kube(i,'get','deployment','legacy' if i=='081' else 'web','-o','json',capture=True).stdout)
            spec=d['spec']['template']['spec']
            configured=(spec.get('dnsPolicy')=='None' and spec.get('dnsConfig',{}).get('nameservers')==['192.0.2.53']) if i=='054' else any(p.get('name')=='http' and p.get('containerPort')==81 for p in spec['containers'][0].get('ports',[]))
        return configured and not check_kube(i)
    return False

def verify_fault(i,wait=120):
    deadline=time.monotonic()+wait
    print('Checking that the intended fault is present (startup and image pulls may take time)...',flush=True)
    while True:
        if fault_observed(i) and not grade(i,samples=1,interval=0):
            work=ROOT/'.lab-state'/i;work.mkdir(parents=True,exist_ok=True)
            (work/'startup.json').write_text(json.dumps({'observed':True,'checked_at':time.time()}))
            print('READY: expected fault confirmed. Investigate first; recovery check should fail until repaired.')
            return 0
        if time.monotonic()>=deadline:
            print('NOT READY: intended fault was not confirmed. Check runtime access, image downloads and live logs; an already repaired lab must be reset. No practice readiness is claimed.')
            return 1
        time.sleep(min(2,max(0,deadline-time.monotonic())))

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

def operate(action,i,samples=3,interval=1,wait=120):
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
            return operate('up',i,wait=wait)
        if i in GIT:
            if not shutil.which('git'):raise RuntimeError('Git is required.')
            if action=='up':
                fresh=not work.exists()
                if fresh:init_git(i,work/'repo')
                print(f'Investigate {work}/repo.')
                return verify_fault(i,wait) if fresh or not (work/'startup.json').exists() else 0
            if action=='down':
                if work.exists():shutil.rmtree(work)
                print('Lab workspace removed.');return 0
        elif i in DOCKER:
            if not shutil.which('docker'):raise RuntimeError('Docker Engine and Compose v2 required.')
            if action=='up':
                fresh=not work.exists()
                work.mkdir(parents=True,exist_ok=True);(work/'empty').mkdir(exist_ok=True)
                source=ROOT/'runnable'/i
                if (source/'assets').exists():shutil.copytree(source/'assets',work/'assets',dirs_exist_ok=True) if not (work/'assets').exists() else None
                target=work/'compose.json'
                if not target.exists():shutil.copyfile(source/'broken.json',target)
                compose(i,'up','-d');print(f'Edit {target} or its assets, then rerun up.')
                return verify_fault(i,wait) if fresh or not (work/'startup.json').exists() else 0
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
                print(f'Investigate namespace devops-lab-{i.lower()}.')
                return verify_fault(i,wait)
            if action=='down':
                if exists:kube(i,'delete','namespace','devops-lab-'+i.lower(),'--wait=false')
                if work.exists():shutil.rmtree(work)
                print('Lab namespace deletion requested; lab data is disposable.');return 0
            if not exists:raise RuntimeError('Run up first.')
        if action=='verify-fault':return verify_fault(i,wait)
        passed=grade(i,samples,interval)
        print(f'PASS: recovery verified across {samples if i not in GIT else 1} checks.' if passed else 'FAIL: recovery or stability criteria not met. Inspect live evidence and retry.')
        return 0 if passed else 1
    except (RuntimeError,OSError,subprocess.TimeoutExpired,ValueError) as error:
        print(f'Lab error: {error}');return 2


