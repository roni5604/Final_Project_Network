from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import time
import threading
import socket

Host = "localhost"
Port = 5604


class NeuralHTTP(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><body><h1>Hello World</h1></body></html>", "utf-8"))

    def do_POST(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        data = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        self.wfile.write(bytes(json.dumps({"time": data}), "utf-8"))


server = HTTPServer((Host, Port), NeuralHTTP)
print("Server started http://%s:%s" % (Host, Port))
server.serve_forever()
server.server_close()
print("Server stopped.")
