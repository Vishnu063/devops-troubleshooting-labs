"""Real disposable CloudLaunch -> Prometheus -> Alertmanager -> Ops Pilot recovery.

No customer target, Jenkins account, Kubernetes cluster or model is used.
"""
import argparse
import importlib.util
import json
import os
from pathlib import Path
import resource
import secrets
import socket
import subprocess
import sys
import tempfile
import threading
import time
from urllib.parse import urlencode
from urllib.request import Request, build_opener, ProxyHandler
from urllib.error import HTTPError

ROOT=Path(__file__).resolve().parents[1]
LABEL='io.ops-pilot.ecosystem-acceptance'
IMAGES={'prometheus':'prom/prometheus:v3.7.0','alertmanager':'prom/alertmanager:v0.28.1','blackbox':'prom/blackbox-exporter:v0.27.0'}


def load(path,name):
    spec=importlib.util.spec_from_file_location(name,path);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module


def port():
    with socket.socket() as sock:sock.bind(('127.0.0.1',0));return sock.getsockname()[1]


def request(url,data=None,headers=None):
    body=None if data is None else json.dumps(data).encode();headers={**(headers or {})}
    if body:headers['Content-Type']='application/json'
    with build_opener(ProxyHandler({})).open(Request(url,data=body,headers=headers),timeout=30) as response:
        raw=response.read(2*1024*1024)
        return json.loads(raw) if 'json' in response.headers.get('Content-Type','') else raw.decode()


def wait_for(check,description,seconds=90):
    end=time.monotonic()+seconds
    while time.monotonic()<end:
        try:
            value=check()
            if value:return value
        except (OSError,ValueError,KeyError,IndexError):pass
        time.sleep(1)
    raise AssertionError('Deadline exceeded: '+description)


def docker(*args):
    return subprocess.check_output(['docker','--host=unix:///var/run/docker.sock',*args],text=True,timeout=150).strip()


def run(cloud,platform,ops,output):
    # Import the reused implementations, not copies of collectors, deployment or approval code.
    sys.path.insert(0,str(ops));from ops_pilot.service import Pilot
    from ops_pilot.ecosystem import EventHub
    from ops_pilot.web import Server
    from triage.ecosystem import envelope,emit
    deployer=load(cloud/'scripts/deploy-ecosystem-demo.py','cloud_deployer')
    token=secrets.token_hex(16);alert_key=secrets.token_urlsafe(32);read_key=secrets.token_urlsafe(32);cloud_key=secrets.token_urlsafe(32)
    os.environ.update(OPS_PILOT_EVENTS_ALERTMANAGER=alert_key,OPS_PILOT_EVENTS_CLOUDLAUNCH=cloud_key,OPS_PILOT_READ_TOKEN=read_key)
    # Explicit local Unix Docker; never inherit a user's remote daemon selector.
    for name in ('DOCKER_HOST','DOCKER_CONTEXT','DOCKER_TLS','DOCKER_TLS_VERIFY','DOCKER_CERT_PATH'):os.environ.pop(name,None)
    stages=[];containers=[];app=None;server=None;thread=None;pilot=None;started=time.monotonic();hub=None
    output.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='ecosystem-acceptance-') as directory:
        private=Path(directory);private.chmod(0o700)
        def record(stage,**detail):stages.append(dict(stage=stage,elapsed_seconds=round(time.monotonic()-started,3),**detail))
        try:
            for image in IMAGES.values():docker('pull',image)
            app=deployer.deploy(cloud);record('CloudLaunch sample deployed',release_id=app['release_id'],image_id=app['image_id'])
            wait_for(lambda:request(app['url']),'sample HTTP readiness',30)
            prom_port,am_port,bb_port=port(),port(),port()
            os.environ['OPS_PILOT_PROMETHEUS_URL']='http://127.0.0.1:'+str(prom_port)
            pilot=Pilot(dict(name='SYNTHETIC ecosystem sample',docker_context='default',container=app['container'],health_url=app['url'],interval_seconds=30),private/'ops')
            hub=EventHub(pilot,private/'ops','ecosystem-demo');server=Server(pilot,0,eventhub=hub)
            thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
            base='http://127.0.0.1:'+str(server.server_port)
            # Native owner session checks are exercised; nothing is authenticated by source tokens as owner.
            owner={'Cookie':'ops_pilot='+server.token,'Origin':base}
            event=envelope('DeploymentEvent','cloudlaunch','ecosystem-demo',{'release_id':app['release_id'],'status':'healthy','image_id':app['image_id']},correlation_id='release-'+app['release_id'])
            emit(event,base+'/webhooks/ecosystem',cloud_key)
            rules=private/'alerts.yml';rules.write_text('groups:\n- name: ecosystem\n  rules:\n  - alert: EcosystemApplicationDown\n    expr: probe_success{job="ecosystem-app"} == 0\n    for: 2s\n    labels:\n      service: ecosystem-demo\n      severity: critical\n')
            am=private/'alertmanager.yml';am.write_text('route:\n  receiver: ops\n  group_by: [alertname,service]\n  group_wait: 1s\n  group_interval: 1s\n  repeat_interval: 1m\nreceivers:\n- name: ops\n  webhook_configs:\n  - url: '+base+'/webhooks/alertmanager\n    send_resolved: true\n    http_config:\n      authorization:\n        type: Bearer\n        credentials_file: /run/keys/alert\n')
            key=private/'alert-key';key.write_text(alert_key);key.chmod(0o600)
            prometheus=private/'prometheus.yml';prometheus.write_text('global:\n  scrape_interval: 1s\n  evaluation_interval: 1s\nrule_files: [/etc/alerts.yml]\nalerting:\n  alertmanagers:\n  - static_configs:\n    - targets: ["127.0.0.1:'+str(am_port)+'"]\nscrape_configs:\n- job_name: ecosystem-app\n  metrics_path: /probe\n  params:\n    module: [http_2xx]\n  static_configs:\n  - targets: ["'+app['url']+'"]\n    labels:\n      service: ecosystem-demo\n  relabel_configs:\n  - source_labels: [__address__]\n    target_label: __param_target\n  - source_labels: [__param_target]\n    target_label: instance\n  - target_label: __address__\n    replacement: "127.0.0.1:'+str(bb_port)+'"\n')
            def start(name,args,mounts):
                command=['run','-d','--name','opsec-'+name+'-'+token,'--label',LABEL+'='+token,'--network','host','--user',str(os.getuid())+':'+str(os.getgid()),'--memory','192m' if name=='prometheus' else '64m','--cpus','0.5','--pids-limit','100','--cap-drop','ALL','--security-opt','no-new-privileges','--tmpfs','/tmp:rw,nosuid,noexec,size=128m']
                for source,target in mounts:command+=['--mount',f'type=bind,src={source},dst={target},readonly']
                cid=docker(*command,IMAGES[name],*args);containers.append(cid)
            start('blackbox',['--config.file=/etc/blackbox.yml','--web.listen-address=127.0.0.1:'+str(bb_port)],[(platform/'monitoring/ecosystem/blackbox.yml','/etc/blackbox.yml')])
            start('alertmanager',['--config.file=/etc/alertmanager.yml','--web.listen-address=127.0.0.1:'+str(am_port),'--cluster.listen-address=','--storage.path=/tmp/am'],[(am,'/etc/alertmanager.yml'),(key,'/run/keys/alert')])
            start('prometheus',['--config.file=/etc/prometheus.yml','--web.listen-address=127.0.0.1:'+str(prom_port),'--storage.tsdb.path=/tmp/prom','--storage.tsdb.retention.time=1h'],[(prometheus,'/etc/prometheus.yml'),(rules,'/etc/alerts.yml')])
            def metric():
                data=request('http://127.0.0.1:'+str(prom_port)+'/api/v1/query?'+urlencode({'query':'probe_success{job="ecosystem-app"}'}))
                values=data.get('data',{}).get('result',[]);return values and float(values[0]['value'][1])==1
            wait_for(metric,'Prometheus observes healthy application');record('Monitoring observes healthy sample')
            # Labs owns controlled failure injection, validates CloudLaunch's ownership first.
            info=json.loads(docker('inspect',app['container']))[0]
            assert info['Config']['Labels'][deployer.LABEL]==app['token']
            docker('stop','--time','3',app['container']);record('Owned test application stopped')
            def detected():
                state=request(base+'/integration/state',headers={'Authorization':'Bearer '+read_key})
                return state['incidents'][0] if state['incidents'] else None
            incident=wait_for(detected,'real Alertmanager delivery')
            record('Prometheus alert received by Ops Pilot',incident_id=incident['id'])
            alert_query=request('http://127.0.0.1:'+str(prom_port)+'/api/v1/query?'+urlencode({'query':'ALERTS{alertname="EcosystemApplicationDown",alertstate="firing"}'}))
            assert alert_query['data']['result'];record('Real firing alert confirmed')
            def action(name):
                current=hub.get(incident['id'])
                return request(base+'/api/ecosystem/action',dict(incident_id=current['id'],revision=current['revision'],action=name,plan_id=current['plan_id']),owner)
            forbidden=dict(incident_id=incident['id'],revision=hub.get(incident['id'])['revision'],action='investigate',plan_id=None)
            for key in (cloud_key,read_key):
                try:request(base+'/api/ecosystem/action',forbidden,{'Authorization':'Bearer '+key})
                except HTTPError as exc:assert exc.code==403
                else:raise AssertionError('Source/read token reached the owner action API')
            failed=action('verify');assert failed['verification']['status']=='failed'
            record('Source/read credentials cannot authorize and failed verification remains failed')
            action('investigate');record('Real native Docker evidence and deterministic diagnosis collected')
            planned=action('plan');assert planned['proposal']['data']['action']['argv'];record('Exact backend restart proposal created')
            try:action('apply')
            except HTTPError as exc:assert exc.code==409
            else:raise AssertionError('Repair was accepted without owner approval')
            assert not json.loads(docker('inspect',app['container']))[0]['State']['Running'];record('No repair before approval verified')
            action('approve');record('Owner approved exact incident plan')
            applied=action('apply')
            print(json.dumps({'recovery_observation':applied.get('execution'),'configured_endpoint':app['url'],'current_port_mapping':docker('port',app['container'],'8080/tcp')}),flush=True)
            assert applied['execution']['infrastructure_status']=='verified';assert applied['execution']['application_health']['healthy'] is True
            record('Allowlisted repair executed; container and HTTP verified')
            wait_for(metric,'healthy Prometheus application probe after repair')
            wait_for(lambda:hub.get(incident['id'])['external_resolved'],'Alertmanager resolution webhook')
            recovered=action('verify');assert recovered['status']=='verified',recovered
            record('HTTP, actual metrics and alert resolution verified',recovery_seconds=recovered['recovery_seconds'])
            # A used approval cannot execute a second time; terminal incident stays read-only.
            try:action('apply')
            except HTTPError as exc:assert exc.code==409
            else:raise AssertionError('Approval replay was accepted')
            report=request(base+'/api/ecosystem/report?id='+incident['id'],headers=owner)
            assert report['type']=='IncidentReport' and not report['data']['unresolved'];assert len(report['data']['timeline'])>=10
            (output/'incident-report.json').write_text(json.dumps(report,indent=2)+'\n');record('Correlated incident report and audit exported')
            # Platform consumes the authenticated read-only integration interface.
            viewer=load(platform/'liveflow/server.py','liveflow_e2e')
            from types import SimpleNamespace
            nodes,_,_=viewer.incident_resources(SimpleNamespace(ops_pilot_url=base));assert nodes and nodes[0]['status']=='healthy'
            record('Platform read-only incident view verified')
            summary=dict(status='pending_cleanup',synthetic=True,customer_changes=False,stages=stages,passed_stages=len(stages),
                main_process_peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                elapsed_seconds=round(time.monotonic()-started,3),limits='No claim that the entire optional stack fits in 8 GB; Grafana/Jenkins/Kind/K8sGPT not started')
            (output/'result.json').write_text(json.dumps(summary,indent=2)+'\n')
        except BaseException:
            (output/'failure.json').write_text(json.dumps({'status':'failed','stages':stages},indent=2)+'\n')
            if hub:(output/'incomplete-state.json').write_text(json.dumps(hub.state(),indent=2)+'\n')
            for index,cid in enumerate(containers):
                try:
                    text=docker('logs','--tail','100',cid)
                    for key in (alert_key,read_key,cloud_key):text=text.replace(key,'[REDACTED]')
                    (output/('monitor-'+str(index)+'.log')).write_text(text[-12000:])
                except (OSError,subprocess.SubprocessError):pass
            raise
        finally:
            cleanup=[]
            if server:server.shutdown();server.server_close();thread.join(timeout=5)
            if pilot:pilot.close()
            for cid in reversed(containers):
                info=json.loads(docker('inspect',cid))[0]
                if info['Config'].get('Labels',{}).get(LABEL)!=token:raise AssertionError('Refusing foreign container cleanup')
                docker('rm','-f',cid);cleanup.append(cid)
            if app:deployer.cleanup(app)
            (output/'cleanup.json').write_text(json.dumps(dict(verified=True,monitoring_containers_removed=len(cleanup),application_removed=app is not None),indent=2)+'\n')
            if (output/'result.json').exists():
                result=json.loads((output/'result.json').read_text());result['status']='passed';result['cleanup_verified']=True
                (output/'result.json').write_text(json.dumps(result,indent=2)+'\n')
    print('Real ecosystem acceptance passed; inspect result, incident report and cleanup evidence. No customer actions occurred.')

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--cloudlaunch',type=Path,required=True);parser.add_argument('--platform',type=Path,required=True);parser.add_argument('--ops-pilot',type=Path,required=True);parser.add_argument('--output',type=Path,required=True);parser.add_argument('--allow-disposable-host',action='store_true');args=parser.parse_args()
    if not args.allow_disposable_host:parser.error('Explicit disposable-host opt-in required')
    run(args.cloudlaunch.resolve(),args.platform.resolve(),args.ops_pilot.resolve(),args.output.resolve())
