import json
import socket
import threading
import time
import string
import random
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer


serverHost = 'localhost'
serverPort = 1234


class NeuralHTTP(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><body><h1>Hello Roni from client</h1></body></html>", "utf-8"))

    def do_POST(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        data = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        self.wfile.write(bytes(json.dumps({"time": data,"name":"roni"}), "utf-8"))



def main():
    print("connecting to HTTP server on port %d" % serverPort)
    httpClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    httpClient.connect((serverHost, serverPort))
    httpClient.send(bytes("GET / HTTP/1.1\r\nHost: localhost\r\n\r\n".encode('utf-8')))
    response = httpClient.recv(4096)
    print("response: %s" % response.decode('utf-8'))



if __name__ == "__main__":
    main()


