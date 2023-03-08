import http.server
import socketserver
import subprocess
import os
import requests

HOST = "localhost"
PORT = 1458


class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            # Serve the index.html page
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('LecturesWebPage.html', 'rb') as f:
                self.wfile.write(f.read())
        elif self.path.startswith('/download') and self.path != '/download':
            if self.path == '/download/Beginner_Tutorial':
                # Download the file from the other server using wget
                url = 'http://localhost:5604/Beginner_Tutorial.txt'
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
                print(f"Downloaded file {file_name} from {url}")
            elif self.path == '/download/Junior_Tuturial':
                # Download the file from the other server using wget
                url = 'http://localhost:5604/Junior_Tutorial.txt'
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
                print(f"Downloaded file {file_name} from {url}")
            elif self.path == '/download/Full_Tuturial':
                # Download the file from the other server using wget
                url = 'http://localhost:5604/Full_Tutorial.txt'
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
                print(f"Downloaded file {file_name} from {url}")
        elif self.path.startswith('/List') and self.path != '/List':
            if self.path == '/List/Student_Lis222t':
                url = 'http://127.0.0.1:1234'
                fileName= 'Server_files/Student_List.txt'
                with requests.get(url) as response:
                    with open(fileName, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=512):
                            if chunk:
                                f.write(chunk)
                f.close()
                self.send_response(200)
                self.send_header('Content-Disposition', f'attachment; filename={fileName}')
                self.send_header('Content-Length', f'{os.path.getsize(fileName)}')
                self.send_header('Content-Type', 'application/octet-stream')
                self.end_headers()
            elif self.path == '/List/Student_List':
                self.send_response(301)
                self.send_header('Location', 'http://127.0.0.1:1234/List/Student_ListDownload')
                self.end_headers()
        return super().do_GET()


Handler = MyHttpRequestHandler

with socketserver.TCPServer((HOST, PORT), Handler) as httpd:
    print("serving at port", PORT)
    print("Server started http://%s:%s" % (HOST, PORT))
    httpd.serve_forever()
