import http.server
import socketserver
import subprocess
import os

HOST = "localhost"
PORT = 9889

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
import requests


class RedirectHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        url_parts = urlparse(self.path)
        if url_parts.path == '/download':
            query = url_parts.query
            params = dict(qc.split("=") for qc in query.split("&"))
            file_url = params.get("file_url")
            if not file_url:
                self.send_error(400, "Missing file_url parameter")
                return
            self.send_response(302)
            self.send_header("Location", file_url)
            self.end_headers()
        else:
            self.send_error(404)


if __name__ == '__main__':
    server_address = ('', PORT)
    httpd = HTTPServer(server_address, RedirectHandler)
    print('Starting HTTP server on port 9889...')
    httpd.serve_forever()
