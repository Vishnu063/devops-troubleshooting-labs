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
