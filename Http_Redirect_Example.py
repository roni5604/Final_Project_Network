import http.server
import urllib.request

class RedirectHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        # Redirect the client to the specified URL
        self.send_response(301)
        self.send_header('Location', 'https://www.gutenberg.org/files/1342/1342-0.txt')
        self.end_headers()

        # Download the file from the redirected URL
        with urllib.request.urlopen('https://www.gutenberg.org/files/1342/1342-0.txt') as response:
            file_contents = response.read()

        # Send the file contents back to the client
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain')
        self.send_header('Content-Disposition', 'attachment; filename="pride-and-prejudice.txt"')
        self.end_headers()
        self.wfile.write(file_contents)


def main():
    httpd = http.server.HTTPServer(('localhost', 8880), RedirectHandler)
    print('Server running on http://localhost:8880')
    httpd.serve_forever()



if __name__ == '__main__':
    main()

