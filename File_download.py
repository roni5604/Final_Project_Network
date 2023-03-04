import http.server
import socketserver
import subprocess
import os

HOST = "localhost"
PORT = 12348


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
        elif self.path.startswith('/list') and self.path != '/list':
            if self.path == '/list/Student_List':
                url = 'http://localhost:5604/list/Student_List'
                file_name = url.split('/')[-1]
                subprocess.call(['wget', url])

                # Redirect the client to open the list of files
                file_path = file_name
                self.send_response(200)
                self.send_header('Content-Disposition', f'attachment; filename={file_name}')
                self.send_header('Content-Length', f'{os.path.getsize(file_path)}')
                self.send_header('Content-Type', 'application/octet-stream')
                self.end_headers()
                with open(file_path, 'rb') as f:
                    self.wfile.write(f.read())
                print(f"Downloaded file {file_name} from {url}")

        return super().do_GET()


Handler = MyHttpRequestHandler

with socketserver.TCPServer((HOST, PORT), Handler) as httpd:
    print("serving at port", PORT)
    print("Server started http://%s:%s" % (HOST, PORT))
    httpd.serve_forever()
