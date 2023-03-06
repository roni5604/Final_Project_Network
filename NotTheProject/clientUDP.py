# Import required modules
import socket

# Define server configuration
HOST = 'localhost'
PORT = 12345

# Create a UDP socket and send a message to the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
message = 'Hello, server!'
client_socket.sendto(message.encode(), (HOST, PORT))

# Receive the response from the server
response, server_address = client_socket.recvfrom(1024)
print(f'Received {len(response)} bytes from {server_address}: {response.decode()}')

# Close the socket
client_socket.close()
