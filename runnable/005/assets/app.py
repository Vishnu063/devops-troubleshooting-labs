import http.server,os,socketserver
class Handler(http.server.BaseHTTPRequestHandler):
 def do_GET(self):
  try:
   value=open('/tmp/lab-private/message').read()
   self.send_response(200);self.end_headers();self.wfile.write(value.encode())
  except PermissionError:
   self.send_response(503);self.end_headers();self.wfile.write(b'Permission denied reading application data')
http.server.HTTPServer(('0.0.0.0',8080),Handler).serve_forever()
