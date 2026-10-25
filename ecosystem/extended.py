"""Owned CI-only Jenkins and Kubernetes failures using Ops Pilot's actual collectors."""
import base64
import http.cookiejar
import json
import os
from pathlib import Path
import secrets
import subprocess
import sys
import tempfile
import time
from urllib.request import Request, build_opener, HTTPCookieProcessor, ProxyHandler
import uuid


def run(args, **kwargs):
    result = subprocess.run(args, text=True, capture_output=True, timeout=kwargs.pop('timeout', 120), **kwargs)
    if result.returncode:
        raise RuntimeError('Owned lab command failed: ' + args[0] + ' (' + str(result.returncode) + ')')
    return result.stdout


def wait(check, seconds=120):
    deadline = time.monotonic() + seconds
    while time.monotonic() < deadline:
        try:
            value = check()
            if value:
                return value
        except (RuntimeError, OSError, ValueError):
            pass
        time.sleep(2)
    raise RuntimeError('Owned lab evidence did not appear within its observation window')


def main():
    if os.environ.get('OPS_PILOT_EXTENDED_LAB') != 'owned-disposable-ci':
        raise SystemExit('Explicit owned disposable CI opt-in required')
    from ops_pilot.diagnostics import Diagnostics
    output = Path(os.environ.get('OPS_PILOT_LAB_OUTPUT', '/work/extended-evidence'))
    output.mkdir(parents=True, exist_ok=True)
    uid = uuid.uuid4().hex[:10]
    label = 'io.ops-pilot.extended=' + uid
    jenkins = 'ops-jenkins-' + uid
    cluster = 'ops-public-' + uid
    context = 'kind-' + cluster
    namespace = 'ops-lab-' + uid
    evidence = {'synthetic': True, 'customer_changes': False, 'status': 'running', 'checks': [], 'cleanup': False}
    cleanup_errors = []
    started = time.monotonic()
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        def desk(tool, conf):
            p = root / 'diagnostics.json'
            p.write_text(json.dumps({'environment': uid, 'tools': {tool: conf}}));p.chmod(0o600)
            return Diagnostics(p, root)
        try:
            # Every service lives inside the enclosing 8 GiB CI container. No host socket or cloud credentials.
            limit = Path('/sys/fs/cgroup/memory.max').read_text().strip()
            if limit != str(8 * 1024**3):
                raise RuntimeError('Expected an enforced enclosing 8 GiB cgroup')
            evidence['memory_limit_bytes'] = int(limit)
            password = secrets.token_urlsafe(32)
            os.environ['OPS_LAB_JENKINS_USER'] = 'lab-owner'
            os.environ['OPS_LAB_JENKINS_PASSWORD'] = password
            init = root / 'security.groovy'
            init.write_text('''import jenkins.model.Jenkins
import hudson.security.*
def j=Jenkins.get()
def realm=new HudsonPrivateSecurityRealm(false)
realm.createAccount("lab-owner", System.getenv("OPS_LAB_JENKINS_PASSWORD"))
j.setSecurityRealm(realm)
def strategy=new FullControlOnceLoggedInAuthorizationStrategy()
strategy.setAllowAnonymousRead(false)
j.setAuthorizationStrategy(strategy)
j.save()
''')
            init.chmod(0o644)
            run(['docker','run','-d','--name',jenkins,'--label',label,'--memory','1536m','--cpus','1',
                 '--network','host','--mount','type=bind,src='+str(init)+',dst=/var/jenkins_home/init.groovy.d/security.groovy,readonly',
                 '-e','JAVA_OPTS=-Djenkins.install.runSetupWizard=false -Xmx512m',
                 '-e','OPS_LAB_JENKINS_PASSWORD','jenkins/jenkins:lts-jdk21','bash','-c',
                 'jenkins-plugin-cli --plugin-download-directory /var/jenkins_home/plugins --plugins workflow-job workflow-cps workflow-durable-task-step pipeline-stage-step && exec /usr/local/bin/jenkins.sh --httpListenAddress=127.0.0.1 --httpPort=18089'], timeout=600)
            base = 'http://127.0.0.1:18089'
            opener = build_opener(ProxyHandler({}), HTTPCookieProcessor(http.cookiejar.CookieJar()))
            authorization = 'Basic ' + base64.b64encode(('lab-owner:' + password).encode()).decode()
            def request(path, data=None, content='application/json'):
                headers = {'Authorization':authorization,'Content-Type':content}
                if data is not None:
                    crumb = json.loads(request('/crumbIssuer/api/json'))
                    headers[crumb['crumbRequestField']] = crumb['crumb']
                with opener.open(Request(base+path, data=data, headers=headers), timeout=10) as response:
                    return response.read(1048576).decode()
            wait(lambda: json.loads(request('/api/json')).get('mode'), 360)
            pipeline = '''<flow-definition plugin="workflow-job"><definition class="org.jenkinsci.plugins.workflow.cps.CpsFlowDefinition" plugin="workflow-cps"><script>node { stage('Owned failure') { sh 'echo permission denied in isolated test; exit 7' } }</script><sandbox>true</sandbox></definition></flow-definition>'''
            request('/createItem?name=owned-failure', pipeline.encode(), 'application/xml')
            request('/job/owned-failure/build', b'')
            wait(lambda: json.loads(request('/job/owned-failure/lastBuild/api/json')).get('result') == 'FAILURE', 120)
            report = desk('jenkins', dict(resource='owned-failure', base_url=base,
                basic_auth={'username_env':'OPS_LAB_JENKINS_USER','password_env':'OPS_LAB_JENKINS_PASSWORD'})).collect('jenkins')
            assert report['status']=='findings' and report['deep_evidence']['log_signals'].get('authorization')
            assert report['actions']==[] and password not in json.dumps(report)
            (output/'jenkins-report.json').write_text(json.dumps(report,indent=2))
            evidence['checks'].append('Real authenticated Jenkins scripted pipeline failure and numbered console signature investigation')
            run(['docker','rm','-f','-v',jenkins]);jenkins=None
            run(['kind','create','cluster','--name',cluster,'--wait','120s'], timeout=240)
            run(['docker','pull','busybox:1.37'], timeout=120)
            run(['kind','load','docker-image','busybox:1.37','--name',cluster], timeout=120)
            def kubectl(*args, document=None):
                return run(['kubectl','--context',context,'--namespace',namespace,*args],input=None if document is None else json.dumps(document))
            kubectl('create','-f','-',document={'apiVersion':'v1','kind':'Namespace','metadata':{'name':namespace,'labels':{'io.ops-pilot.lab':uid}}})
            def deployment(name, command, **fields):
                container={'name':'app','image':'busybox:1.37','imagePullPolicy':'IfNotPresent','command':command,**fields}
                return {'apiVersion':'apps/v1','kind':'Deployment','metadata':{'name':name},'spec':{'replicas':1,'progressDeadlineSeconds':20,
                    'selector':{'matchLabels':{'app':name}},'template':{'metadata':{'labels':{'app':name}},'spec':{'containers':[container]}}}}
            cases=[('crash',['sh','-c','exit 7'],{},'kubernetes:crash-loop'),
                   ('image',['sleep','3600'],{'image':'invalid.invalid/ops-pilot/never:missing'},'kubernetes:image-pull'),
                   ('oom',['sh','-c','x=$(head -c 64000000 /dev/zero | tr "\\000" x); sleep 3600'],{'resources':{'limits':{'memory':'16Mi'}}},'kubernetes:oom'),
                   ('pending',['sleep','3600'],{'resources':{'requests':{'cpu':'1000'}}},'kubernetes:scheduling'),
                   ('rollout',['sleep','3600'],{'readinessProbe':{'exec':{'command':['sh','-c','exit 1']},'periodSeconds':1}},'kubernetes:reason')]
            for name,command,fields,code in cases:
                kubectl('apply','-f','-',document=deployment(name,command,**fields))
                collector=desk('kubernetes',{'context':context,'namespace':namespace,'resource':name})
                def observed():
                    report=collector.collect('kubernetes')
                    return report if code in {f['code'] for f in report.get('findings',[])} else None
                report=wait(observed,150)
                assert report['actions']==[]
                (output/(name+'-report.json')).write_text(json.dumps(report,indent=2))
                evidence['checks'].append('Real Kubernetes '+name+' observed by native Ops Pilot diagnostics')
                kubectl('delete','deployment',name,'--wait=true','--timeout=45s')
            evidence['status']='passed'
        finally:
            if jenkins:
                try:
                    obj=json.loads(run(['docker','inspect',jenkins]))[0]
                    if obj['Config']['Labels'].get('io.ops-pilot.extended')!=uid:raise RuntimeError('Ownership changed')
                    run(['docker','rm','-f','-v',jenkins])
                except Exception:cleanup_errors.append('Jenkins cleanup was not verified')
            try:
                nodes=run(['kind','get','nodes','--name',cluster]).split()
                if nodes:
                    run(['kind','delete','cluster','--name',cluster],timeout=120)
                    if run(['kind','get','nodes','--name',cluster]).strip():raise RuntimeError('Cluster remains')
            except Exception:cleanup_errors.append('Kind cleanup was not verified')
            evidence['cleanup']=not cleanup_errors
            evidence['cleanup_errors']=cleanup_errors
            evidence['elapsed_seconds']=round(time.monotonic()-started,3)
            peak=Path('/sys/fs/cgroup/memory.peak')
            evidence['enclosing_cgroup_peak_bytes']=int(peak.read_text()) if peak.exists() else None
            if cleanup_errors:evidence['status']='failed'
            (output/'extended-result.json').write_text(json.dumps(evidence,indent=2))
            print(json.dumps(evidence,indent=2),flush=True)
    if evidence['status']!='passed' or not evidence['cleanup']:raise SystemExit(1)


if __name__=='__main__':main()
