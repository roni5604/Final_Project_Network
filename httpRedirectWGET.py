import http.server
import socketserver
import subprocess
import os

class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            # Serve the index.html page
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('index.html', 'rb') as f:
                self.wfile.write(f.read())
        elif self.path == '/download':
            # Download the file from the other server using wget
            url = 'https://filesamples.com/samples/document/txt/sample3.txt'
            file_name = url.split('/')[-1]
            subprocess.call(['wget', url])

            # Redirect the client to the downloaded file
            file_path = file_name
            self.send_response(200)
            self.send_header('Content-Disposition', f'attachment; filename={file_name}')
            self.send_header('Content-Length', f'{os.path.getsize(file_path)}')
            self.send_header('Content-Type', 'application/octet-stream')
            self.end_headers()
            with open(file_path, 'rb') as f:
                self.wfile.write(f.read())


PORT = 8000

Handler = MyHttpRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()
