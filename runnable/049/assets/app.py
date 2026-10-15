import http.server,os,socket
class Handler(http.server.BaseHTTPRequestHandler):
 def do_GET(self):
  try:
   with socket.create_connection((os.environ['DB_HOST'],6379),timeout=2) as conn:
    conn.sendall(b'*3\r\n$3\r\nSET\r\n$8\r\nlabcheck\r\n$9\r\nrecovered\r\n')
    if conn.recv(128)!=b'+OK\r\n':raise RuntimeError('write failed')
    conn.sendall(b'*2\r\n$3\r\nGET\r\n$8\r\nlabcheck\r\n')
    if b'recovered' not in conn.recv(128):raise RuntimeError('read failed')
   self.send_response(200);self.end_headers();self.wfile.write(b'database-roundtrip-ok')
  except Exception as error:
   self.send_response(503);self.end_headers();self.wfile.write(str(error).encode())
http.server.HTTPServer(('0.0.0.0',8080),Handler).serve_forever()
