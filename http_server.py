import socket
import threading
import time
import json
import queue
import random
import string
from http.server import BaseHTTPRequestHandler, HTTPServer


HOST = "localhost"
PORT = 1234
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind((HOST, PORT))
serverSocket.listen(5)


class NeuralHTTP(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><body><h1>Hello World and Elor</h1></body></html>", "utf-8"))

    def do_POST(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        data = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        self.wfile.write(bytes(json.dumps({"time": data}), "utf-8"))



def main():
    clientSocket, address = serverSocket.accept()
    httpd = HTTPServer((HOST, PORT), NeuralHTTP)
    print("----------------------------------")
    print('Server running on http://localhost:8880')
    httpd.serve_forever()
    print(f"Connection established with {address}")
    print(clientSocket.recv(1024).decode())
    clientSocket.send(
        bytes("HTTP/1.1 200 OK \r\n\r\n<html><body><h1>Hello World from http server</h1></body></html>", "utf-8"))


if __name__ == "__main__":
    main()
