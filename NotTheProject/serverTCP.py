# Import required modules
import socket
import http.server
import threading

# Define server configuration
HOST = 'localhost'
PORT = 3477


# Define handler for HTTP requests
class RequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Set response headers
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        # Send response body
        self.wfile.write(b'<html><body><h1>Hello, world!</h1></body></html>')


# Define function to start the server
def start_server():
    server_address = (HOST, PORT)
    httpd = http.server.HTTPServer(server_address, RequestHandler)
    print(f'Starting server on http://{HOST}:{PORT}...')
    httpd.serve_forever()


# Start the server in a separate thread
server_thread = threading.Thread(target=start_server)
server_thread.start()

# Listen for TCP connections
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)
print(f'Listening on tcp://{HOST}:{PORT}...')

# Accept a client connection
client_socket, address = server_socket.accept()
print(f'Accepted connection from {address}')

# Receive data from the client
data = client_socket.recv(1024)
print(f'Received data from client: {data.decode()}')

# Send a response to the client
response = 'HTTP/1.1 200 OK\r\nContent-type: text/html\r\n\r\n<html><body><h1>Hello, world!</h1></body></html>'
client_socket.sendall(response.encode())

# Close the client socket and server socket
client_socket.close()
server_socket.close()
