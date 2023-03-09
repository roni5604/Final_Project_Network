import socket
from consts import PROXY_HOST, PROXY_PORT


# create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect to the proxy server
client_socket.connect((PROXY_HOST, PROXY_PORT))

# send a GET request for the file "test.html"
request_data = b'GET /TCP_appliction/test.txt HTTP/1.1\r\nHost: localhost:5604\r\n\r\n'
client_socket.sendall(request_data)

# receive the response data from the proxy server
response_data = b''
while True:
    data = client_socket.recv(1024)
    if not data:
        break
    response_data += data

# print the response data
print(response_data.decode())

# close the client socket
client_socket.close()
