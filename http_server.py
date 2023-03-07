import http
import socket
import threading
import time
import json
import queue
import random
import string
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.request
import subprocess
import socketserver

HOST = "localhost"
PORT = 1234

data = []


class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            # Serve the index.html page
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('downloadLink.html', 'rb') as f:
                self.wfile.write(f.read())
        if self.path == '/redirect':
            self.send_response(302)
            self.send_header('Location', '/download')
            self.end_headers()
        elif self.path == '/download':
            url = 'http://localhost:1234/file.txt'  # URL of the file to download
            filename = 'StudentList.txt'  # Name of the file to save
            with urllib.request.urlopen(url) as response, open(filename, 'wb') as out_file:
                CHUNK_SIZE = 512  # Number of bytes to read at a time
                while True:
                    chunk = response.read(CHUNK_SIZE)
                    if not chunk:
                        break
                    out_file.write(chunk)
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.send_header('Content-Disposition', 'attachment; filename="file.txt"')
            self.end_headers()
            with open(filename, 'rb') as f:
                CHUNK_SIZE = 512  # Number of bytes to read at a time
                while True:
                    chunk = f.read(CHUNK_SIZE)
                    if not chunk:
                        break
                    self.wfile.write(chunk)
        else:
            self.send_response(404)  # Not Found
            self.end_headers()

        return super().do_GET()


with socketserver.TCPServer((HOST, PORT), MyHttpRequestHandler) as server_sock:
    print("----------------------------------")
    print("Server  running on http://%s:%s" % (HOST, PORT))
    print("----------------------------------")
    server_sock.serve_forever()
