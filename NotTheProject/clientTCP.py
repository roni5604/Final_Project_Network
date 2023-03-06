# Import required modules
import socket

# Define server configuration
HOST = 'localhost'
PORT = 3477

# Create a TCP socket and connect to the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

# Send a GET request to the server
request = 'GET / HTTP/1.1\r\nHost: localhost\r\n\r\n'
client_socket.sendall(request.encode())

# Receive the response from the server
response = client_socket.recv(1024)
print(f'Received response from server: {response.decode()}')

# Close the socket
client_socket.close()
