import socket
from consts import PROXY_HOST, PROXY_PORT, FILES_SERVER_HOST, FILES_SERVER_PORT

# create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# bind the socket to a public host and port
server_socket.bind((PROXY_HOST, PROXY_PORT))

# listen for incoming connections
server_socket.listen(1)

print(f'Serving as a proxy on {PROXY_HOST}:{PROXY_PORT}...')

while True:
    # accept incoming client connections
    client_connection, client_address = server_socket.accept()

    # get the request data
    request_data = client_connection.recv(1024).decode()

    # parse the request data
    request_lines = request_data.split('\r\n')
    request_line = request_lines[0]
    if len(request_line) == 0:
        continue
    request_method, path, http_version = request_line.split(" ")

    location_header = f'Location: http://{FILES_SERVER_HOST}:{FILES_SERVER_PORT}{path}\r\n'

    # construct the response data for a 301 redirect
    response_headers = [
        'HTTP/1.1 301 Moved Permanently',
        location_header,
        'Connection: close',
        '',
        ''
    ]
    response_data = '\r\n'.join(response_headers).encode()
    # send the response data back to the client
    client_connection.sendall(response_data)

    # close the client connection
    client_connection.close()
