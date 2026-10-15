import http.server
class Handler(http.server.BaseHTTPRequestHandler):
 def do_GET(self):
  self.send_response(200);self.end_headers();self.wfile.write(b'lab_requests_total 42\n')
http.server.HTTPServer(('0.0.0.0',9100),Handler).serve_forever()
