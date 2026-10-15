"""Regression: Prometheus 3 requires an explicit supported metrics media type."""
import http.server,runpy,sys,threading,unittest,urllib.request
from pathlib import Path
from unittest.mock import patch,MagicMock
ROOT=Path(__file__).resolve().parents[1]

class MetricsEndpointTests(unittest.TestCase):
 def test_real_http_response_declares_metrics_format(self):
  server_class=http.server.HTTPServer
  with patch.object(http.server,'HTTPServer',return_value=MagicMock()) as constructor:
   runpy.run_path(str(ROOT/'runnable/033/assets/metrics.py'))
   handler=constructor.call_args.args[1]
  server=server_class(('127.0.0.1',0),handler)
  thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
  try:
   opener=urllib.request.build_opener(urllib.request.ProxyHandler({}))
   with opener.open(f'http://127.0.0.1:{server.server_port}/metrics',timeout=3) as response:
    self.assertEqual(response.status,200)
    self.assertEqual(response.headers['Content-Type'],'text/plain; version=0.0.4')
    self.assertEqual(response.read(),b'lab_requests_total 42\n')
  finally:server.shutdown();thread.join(timeout=3);server.server_close()

if __name__=='__main__':unittest.main()

class MonitoringGraderTests(unittest.TestCase):
 def test_checks_intended_target_despite_old_series_and_rejects_current_failure(self):
  import json,sys,urllib.parse
  sys.path.insert(0,str(ROOT/'scripts'))
  import native
  state={'up':1}
  class Api(http.server.BaseHTTPRequestHandler):
   def do_GET(self):
    query=urllib.parse.parse_qs(urllib.parse.urlsplit(self.path).query)['query'][0]
    if query.startswith('up'):
     results=[{'metric':{'instance':'metrics:9100'},'value':[1,str(state['up'])]}]
     if 'instance=' not in query:results.insert(0,{'metric':{'instance':'metrics:9091'},'value':[1,'0']})
    else:results=[{'metric':{'instance':'metrics:9100'},'value':[1,'42']}]
    self.send_response(200);self.send_header('Content-Type','application/json');self.end_headers();self.wfile.write(json.dumps({'status':'success','data':{'result':results}}).encode())
   def log_message(self,*args):pass
  server=http.server.HTTPServer(('127.0.0.1',0),Api);thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
  info={'Id':'stable-container','RestartCount':0,'State':{'Running':True,'StartedAt':'unchanged'},'NetworkSettings':{'Ports':{'9090/tcp':[{'HostIp':'127.0.0.1','HostPort':str(server.server_port)}]}}}
  try:
   with patch.object(native,'docker_info',return_value=info):
    self.assertTrue(native.grade('033',samples=3,interval=0))
    state['up']=0
    self.assertFalse(native.grade('033',samples=3,interval=0))
  finally:server.shutdown();thread.join(timeout=3);server.server_close()
