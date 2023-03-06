import random
import requests
from http.server import HTTPServer, BaseHTTPRequestHandler

PORT = 8998


# Server 1 - makes request for file
class Client:
    def __init__(self, url):
        self.url = url

    def get_file(self):
        response = requests.get(self.url)
        return response.text


files = ["file1.txt", "file2.txt", "file3.txt"]
file = files[random.randint(0, 2)]
client = Client(f"http://localhost:{PORT}/{file}")
file_contents = client.get_file()
print(file_contents)


# Server 2 - serves file requested by Server 1 (send the file)
class Server(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/file1.txt":
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            with open("file1.txt", "rb") as f:
                self.wfile.write(f.read())
        elif self.path == "/file2.txt":
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            with open("file2.txt", "rb") as f:
                self.wfile.write(f.read())
        elif self.path == "/file3.txt":
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            with open("file3.txt", "rb") as f:
                self.wfile.write(f.read())
        else:
            self.send_error(404)


server_address = ("", PORT)
httpd = HTTPServer(server_address, Server)
httpd.serve_forever()

## really basic option...
# class Server(BaseHTTPRequestHandler):
#     def do_GET(self):
#         if self.path == "/file.txt":
#             self.send_response(200)
#             self.send_header("Content-type", "text/plain")
#             self.end_headers()
#             with open("file.txt", "rb") as f:
#                 self.wfile.write(f.read())
#         else:
#             self.send_error(404)
#
#
# server_address = ("", PORT)
# httpd = HTTPServer(server_address, Server)
# httpd.serve_forever()
