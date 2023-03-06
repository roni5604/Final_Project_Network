# Import required modules
import socket

# Define server configuration
HOST = 'localhost'
PORT = 12345

# Create a UDP socket and bind it to the server address
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = (HOST, PORT)
server_socket.bind(server_address)
print(f'Listening on udp://{HOST}:{PORT}...')

# Receive data from the client and send a response
while True:
    data, client_address = server_socket.recvfrom(1024)
    print(f'Received {len(data)} bytes from {client_address}: {data.decode()}')
    response = 'Hello, client!'
    server_socket.sendto(response.encode(), client_address)
