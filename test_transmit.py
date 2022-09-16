import time
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from pydantic import BaseModel

from typing import Any


class Reading(BaseModel):
  id: str
  device: str
  value: dict[str, Any]
  timestamp: Optional[str] # TODO datetime


HOST = '0.0.0.0'
PORT = 8000

class MyHandler(BaseHTTPRequestHandler):
  def do_HEAD(s):
    s.send_response(200)
    s.send_header("Content-type", "text/html")
    s.end_headers()

  def do_GET(s):
    s.send_response(200)
    s.send_header("Content-type", "text/html")
    s.end_headers()

  def do_POST(s):
    length = int(s.headers['Content-Length'])
    post_data = json.loads(s.rfile.read(length)) #.decode('utf-8')
    reading = Reading(**post_data)
    print(reading)
    s.send_response(200)
    s.send_header("Content-type", "text/html")
    s.end_headers()
    ...


if __name__ == '__main__':
  httpd = HTTPServer((HOST, PORT), MyHandler)
  print(time.asctime(), "Server Starts - %s:%s" % (HOST, PORT))
  try:
    httpd.serve_forever()
  except KeyboardInterrupt:
    pass
  httpd.server_close()
  print(time.asctime(), "Server Stops - %s:%s" % (HOST, PORT))