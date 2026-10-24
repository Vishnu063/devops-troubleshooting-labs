#!/usr/bin/env python3
"""Disposable, opt-in CloudLaunch → Prometheus → Pilot → approved recovery lab.

Run with sibling checkouts and their Python dependencies installed. No EC2,
Kubernetes, paid AI, production config, or existing application is targeted.
"""
import argparse
import base64
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import secrets
import socket
import subprocess
import sys
import threading
import time
from urllib.error import URLError
from urllib.request import Request, build_opener, ProxyHandler
import uuid


def free_port():
    with socket.socket() as sock:
        sock.bind(('127.0.0.1', 0))
        return sock.getsockname()[1]


def wait(check, description, seconds=90):
    deadline = time.monotonic() + seconds
    while time.monotonic() < deadline:
        try:
            value = check()
            if value:
                return value
        except (OSError, ValueError, KeyError, IndexError, URLError):
            pass
        time.sleep(.5)
    raise RuntimeError('Timed out: ' + description)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workspace', type=Path, required=True)
    parser.add_argument('--tools', type=Path, required=True, help='Directory containing trusted prometheus, promtool, alertmanager, amtool binaries')
    parser.add_argument('--output', type=Path, required=True, help='Private result directory outside Git')
    parser.add_argument('--allow-disposable-failure', action='store_true')
    parser.add_argument('--grafana-home', type=Path, help='Optional trusted Grafana distribution; disabled by default')
    parser.add_argument('--skip-build', action='store_true', help='Reuse only an image tagged for this exact source tree hash')
    args = parser.parse_args()
    if not args.allow_disposable_failure:
        parser.error('Explicit --allow-disposable-failure is required')
    root = args.workspace.resolve()
    cloud = root / 'cloudlaunch'
    platform = root / 'devops_platform'
    for name in ['ops-pilot', 'devops-triage-assistant']:
        sys.path.insert(0, str(root / name))
    from ops_pilot.service import Pilot
    from ops_pilot.web import Server
    from ops_pilot.events_client import send
    from triage.health import check_health
    args.output.mkdir(parents=True, exist_ok=True, mode=0o700)
    os.chmod(args.output, 0o700)
    prefix = 'ecosystem-lab-' + uuid.uuid4().hex[:10]
    processes, resources, threads, streams = [], [], [], []
    result = {'status': 'failed', 'lab_id': prefix, 'checks': [], 'started_at': datetime.now(timezone.utc).isoformat()}
    started = time.monotonic()
    def record(name):
        result['checks'].append(name)
        print('PASS:', name, flush=True)
    def docker(*parts, timeout=180):
        return subprocess.check_output(['docker', '--context', 'default', *parts], text=True, timeout=timeout).strip()
    def get(url):
        with build_opener(ProxyHandler({})).open(url, timeout=3) as response:
            return json.loads(response.read(1024 * 1024))
    def launch(binary, *parts):
        stream = (args.output / (binary + '.log')).open('w'); streams.append(stream)
        process = subprocess.Popen([str(args.tools.resolve() / binary), *parts], stdout=stream, stderr=subprocess.STDOUT)
        processes.append(process)
        return process
    def marker_file(path, text):
        path.write_text(text); path.chmod(0o600)
    try:
        endpoint = docker('context', 'inspect', 'default', '--format', '{{.Endpoints.docker.Host}}')
        if endpoint != 'unix:///var/run/docker.sock':
            raise RuntimeError('Lab requires the managed local Docker socket')
        # Hash the actual build inputs, including uncommitted reviewed changes.
        digest = hashlib.sha256()
        inputs = [cloud / 'Dockerfile', cloud / 'requirements.txt'] + sorted(p for p in (cloud / 'app').rglob('*') if p.is_file() and p.suffix not in {'.pyc'} and '__pycache__' not in p.parts)
        for path in inputs:
            digest.update(str(path.relative_to(cloud)).encode()); digest.update(path.read_bytes())
        release = digest.hexdigest()
        image = 'cloudlaunch-ecosystem:' + release[:24]
        if args.skip_build:
            docker('image', 'inspect', image)
        else:
            command = ['docker', '--context', 'default', 'build', '--secret', 'id=proxy_ca,src=/etc/ssl/certs/ca-certificates.crt', '-t', image, str(cloud)]
            with (args.output / 'build.log').open('w') as log:
                subprocess.run(command, check=True, stdout=log, stderr=subprocess.STDOUT, timeout=600)
        result['release_id'] = release
        result['image_id'] = docker('image', 'inspect', image, '--format', '{{.Id}}')
        app_port, db_port, prom_port, am_port = [free_port() for _ in range(4)]
        env = dict(os.environ, LAB_DB_PASSWORD=secrets.token_hex(24), LAB_ADMIN_HASH='lab-disabled-login',
                   LAB_SESSION_SECRET=secrets.token_hex(32), LAB_APP_PORT=str(app_port), LAB_DB_PORT=str(db_port), LAB_APP_IMAGE=image, LAB_RELEASE_ID=release)
        compose = ['docker', '--context', 'default', 'compose', '--profile', 'ecosystem-lab', '-p', prefix, '-f', str(cloud / 'integrations/compose.lab.yml')]
        resources.append(('compose', compose, env))
        subprocess.run(compose + ['up', '-d', '--wait', '--wait-timeout', '90'], env=env, check=True, timeout=180)
        container = subprocess.check_output(compose + ['ps', '-q', 'app'], env=env, text=True).strip()
        target = json.loads(docker('inspect', container))[0]
        service = target['Name'].lstrip('/')
        url = f'http://127.0.0.1:{app_port}/health'
        assert get(url)['database'] == 'connected'
        record('CloudLaunch app deployed with live PostgreSQL readiness')
        pilot = Pilot(dict(name='Disposable CloudLaunch', docker_context='default', container=service, health_url=url, interval_seconds=15), args.output / 'state')
        assert pilot.tick() and pilot.monitor['healthy'] is True
        server = Server(pilot, 0, ingest_token=secrets.token_urlsafe(32))
        resources.append(('server', server, pilot))
        thread = threading.Thread(target=server.serve_forever, daemon=True); thread.start(); threads.append(thread)
        pilot_port = server.server_port
        token_file = args.output / 'ingest-token'
        marker_file(token_file, server.ingest_token)
        event_url = f'http://127.0.0.1:{pilot_port}/api/events'
        stamp = datetime.now(timezone.utc).isoformat()
        deployment = dict(schema_version=1, kind='DeploymentEvent', id=prefix+':deployment', source='cloudlaunch', service=service, timestamp=stamp, correlation_id=prefix, status='succeeded', release_id=result['image_id'])
        assert not send(event_url, server.ingest_token, deployment)['receipts'][0]['duplicate']
        assert send(event_url, server.ingest_token, deployment)['receipts'][0]['duplicate']
        record('Authenticated deployment event and duplicate receipt')
        replacements = {'APP_PORT': str(app_port), 'PILOT_PORT': str(pilot_port), 'ALERTMANAGER_PORT': str(am_port), 'SERVICE_NAME': service, 'TOKEN_FILE': str(token_file), 'RULES_FILE': str(args.output.resolve() / 'alerts.yml')}
        for name in ['prometheus.yml', 'alerts.yml', 'alertmanager.yml']:
            content = (platform / 'monitoring/ecosystem' / name).read_text()
            for key, value in replacements.items(): content = content.replace(key, value)
            marker_file(args.output / name, content)
        for binary, parts in [('promtool', ['check', 'config', str(args.output/'prometheus.yml')]), ('amtool', ['check-config', str(args.output/'alertmanager.yml')])]:
            subprocess.run([str(args.tools / binary), *parts], check=True, stdout=subprocess.DEVNULL)
        launch('alertmanager', '--config.file='+str(args.output/'alertmanager.yml'), '--storage.path='+str(args.output/'am-data'), '--web.listen-address=127.0.0.1:'+str(am_port), '--cluster.listen-address=')
        launch('prometheus', '--config.file='+str(args.output/'prometheus.yml'), '--storage.tsdb.path='+str(args.output/'prom-data'), '--storage.tsdb.retention.time=1h', '--web.listen-address=127.0.0.1:'+str(prom_port))
        prom = f'http://127.0.0.1:{prom_port}'
        wait(lambda: get(prom+'/api/v1/query?query=up%7Bjob%3D%22cloudlaunch-ecosystem%22%7D')['data']['result'][0]['value'][1] == '1', 'healthy Prometheus target')
        record('Real Prometheus scrape sees healthy CloudLaunch')
        grafana_get = None
        if args.grafana_home:
            grafana_port = free_port()
            provision = args.output / 'grafana-provisioning'
            (provision/'datasources').mkdir(parents=True)
            (provision/'dashboards').mkdir()
            marker_file(provision/'datasources/prometheus.yml', 'apiVersion: 1\ndatasources:\n  - name: Prometheus\n    uid: prometheus\n    type: prometheus\n    access: proxy\n    url: '+prom+'\n    isDefault: true\n')
            marker_file(provision/'dashboards/ecosystem.yml', 'apiVersion: 1\nproviders:\n  - name: ecosystem\n    type: file\n    options:\n      path: '+str((platform/'monitoring/ecosystem').resolve())+'\n')
            password = secrets.token_urlsafe(32)
            grafana_env = dict(os.environ, GOMAXPROCS='2', GF_SERVER_HTTP_ADDR='127.0.0.1', GF_SERVER_HTTP_PORT=str(grafana_port),
                GF_SECURITY_ADMIN_USER='lab-owner', GF_SECURITY_ADMIN_PASSWORD=password, GF_USERS_ALLOW_SIGN_UP='false',
                GF_PATHS_DATA=str(args.output.resolve()/'grafana-data'), GF_PATHS_LOGS=str(args.output.resolve()/'grafana-logs'),
                GF_PATHS_PLUGINS=str(args.output.resolve()/'grafana-plugins'), GF_PATHS_PROVISIONING=str(provision.resolve()),
                GF_ANALYTICS_REPORTING_ENABLED='false', GF_ANALYTICS_CHECK_FOR_UPDATES='false', GF_ANALYTICS_CHECK_FOR_PLUGIN_UPDATES='false',
                GF_PLUGINS_PREINSTALL_DISABLED='true', GF_UNIFIED_ALERTING_ENABLED='false')
            stream = (args.output/'grafana.log').open('w'); streams.append(stream)
            processes.append(subprocess.Popen([str(args.grafana_home.resolve()/'bin/grafana'), 'server', '--homepath', str(args.grafana_home.resolve())],
                env=grafana_env, stdout=stream, stderr=subprocess.STDOUT))
            def grafana_get(path):
                auth = base64.b64encode(('lab-owner:'+password).encode()).decode()
                request = Request(f'http://127.0.0.1:{grafana_port}'+path, headers={'Authorization': 'Basic '+auth})
                with build_opener(ProxyHandler({})).open(request, timeout=3) as response:
                    return json.loads(response.read(1024*1024))
            wait(lambda: grafana_get('/api/health')['database']=='ok', 'Grafana database')
            dashboard = wait(lambda: grafana_get('/api/dashboards/uid/devops-ecosystem'), 'provisioned ecosystem dashboard')
            assert len(dashboard['dashboard']['panels']) == 6
            value = grafana_get('/api/datasources/proxy/uid/prometheus/api/v1/query?query=up%7Bjob%3D%22cloudlaunch-ecosystem%22%7D')
            assert value['data']['result'][0]['value'][1] == '1'
            record('Authenticated Grafana provisioned six panels and queried live CloudLaunch health through Prometheus')
        docker('stop', '--time', '1', container)
        record('Stopped only the labelled disposable application')
        wait(lambda: any(a['labels']['alertname'] == 'CloudLaunchApplicationDown' and a['state']=='firing' for a in get(prom+'/api/v1/alerts')['data']['alerts']), 'real alert firing')
        record('Real Prometheus application-down alert firing')
        wait(lambda: any(row['event']['kind']=='MonitoringAlert' and row['event']['status']=='firing' and row['incident_id'] for row in pilot.events.history()), 'Alertmanager delivery and evidence collection')
        assert pilot.report['snapshot']['observations']['state'] == ['exited']
        assert pilot.report['findings']
        assert pilot.export_report()['structured_diagnosis']['evidence']
        record('Alertmanager delivered alert; Pilot collected real evidence and Triage diagnosis')
        plan = pilot.action('plan')
        try:
            pilot.action('apply', plan['id'])
        except ValueError:
            pass
        else:
            raise AssertionError('Unapproved repair executed')
        assert json.loads(docker('inspect', container))[0]['State']['Status'] == 'exited'
        record('Unapproved repair refused and application remained stopped')
        # This command-line flag authorizes this runner's fixed disposable restart
        # policy only; the ordinary webhook has no approval authority.
        pilot.action('approve', plan['id'])
        assert json.loads(docker('inspect', container))[0]['State']['Status'] == 'exited'
        record('Explicit disposable-lab approval alone did not execute')
        outcome = pilot.action('apply', plan['id'])
        marker_file(args.output/'repair-outcome.json', json.dumps(outcome, indent=2)+'\n')
        assert outcome['status'] == 'verified' and outcome['application_health']['healthy'] is True
        assert get(url)['status'] == 'healthy'
        record('Allowlisted restart passed container identity and live HTTP/database verification')
        try:
            pilot.action('apply', plan['id'])
        except ValueError:
            pass
        else:
            raise AssertionError('Replayed approval executed')
        record('Consumed approval replay refused')
        wait(lambda: not any(a['labels']['alertname']=='CloudLaunchApplicationDown' and a['state']=='firing' for a in get(prom+'/api/v1/alerts')['data']['alerts']), 'Prometheus alert resolution')
        wait(lambda: any(row['event']['status']=='resolved' for row in pilot.events.history()), 'resolved webhook delivered')
        record('Prometheus alert resolved and Alertmanager resolution received')
        report = pilot.export_report()
        assert report['result']['status'] == 'verified'
        assert report['history'] and report['event_audit'] and report['incoming_events']
        marker_file(args.output/'incident-report.json', json.dumps(report, indent=2)+'\n')
        result['docker_stats'] = docker('stats', '--no-stream', '--format', '{{json .}}', container)
        result['monitoring_versions'] = {binary: subprocess.check_output([str(args.tools/binary),'--version'],stderr=subprocess.STDOUT,text=True).splitlines()[0] for binary in ['prometheus','alertmanager']}
        record('Incident report contains evidence, action history, receipts and owner audit')
        if grafana_get:
            value = grafana_get('/api/datasources/proxy/uid/prometheus/api/v1/query?query=up%7Bjob%3D%22cloudlaunch-ecosystem%22%7D')
            assert value['data']['result'][0]['value'][1] == '1'
            record('Grafana datasource sees recovered application')
        result['process_peak_rss_kib'] = {}
        for process in processes:
            fields = Path(f'/proc/{process.pid}/status').read_text().splitlines()
            result['process_peak_rss_kib'][str(process.pid)] = next((line.split(':',1)[1].strip() for line in fields if line.startswith('VmHWM:')), 'unknown')
        result['status'] = 'verified' 
        result['limitations'] = ['The runner deploys through Compose; Jenkins execution is established separately by controller build evidence.', 'No Kubernetes/Argo CD/Helm/K8sGPT live validation.', 'No browser visual acceptance or total 8 GB capacity claim.']
        return 0
    except Exception as error:
        result['error_type'] = type(error).__name__
        print('FAIL:', type(error).__name__, 'See private logs and result.json', file=sys.stderr)
        return 1
    finally:
        for process in reversed(processes):
            process.terminate()
            try: process.wait(timeout=10)
            except subprocess.TimeoutExpired: process.kill(); process.wait()
        for kind, obj, config in reversed(resources):
            if kind == 'server':
                obj.shutdown(); obj.server_close(); config.close()
            else:
                # The exact generated project has no production container names,
                # mounts or external volumes. No caller-supplied project accepted.
                subprocess.run(obj+['down','--volumes','--remove-orphans'],env=config,check=False,timeout=90,stdout=subprocess.DEVNULL)
        for thread in threads: thread.join(timeout=3)
        for stream in streams: stream.close()
        token = args.output/'ingest-token'
        token.unlink(missing_ok=True)
        result['elapsed_seconds'] = round(time.monotonic()-started, 2)
        marker_file(args.output/'result.json', json.dumps(result, indent=2)+'\n')


if __name__ == '__main__':
    raise SystemExit(main())
