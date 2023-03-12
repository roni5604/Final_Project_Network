import socket
from consts import PROXY_HOST, PROXY_PORT, FILES_SERVER_HOST, FILES_SERVER_PORT
from helpers import to_html_format_Redirect

# function to run our proxy
def main_proxy():
    # create a TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # set the socket to unblocking mode to multiply use of the connection
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # bind the socket to our host and port
    server_socket.bind((PROXY_HOST, PROXY_PORT))

    # listen for incoming connections
    server_socket.listen(1)

    print(f'Serving as a proxy on {PROXY_HOST}:{PROXY_PORT}...')

    while True:
        # accept incoming client connections
        client_connection, client_address = server_socket.accept()

        # get the request data as string
        request_data = client_connection.recv(1024).decode()

        # parse the request data
        request_lines = request_data.split('\r\n')
        request_line = request_lines[0]
        if len(request_line) == 0:
            continue
        request_method, path, http_version = request_line.split(" ")
        # set the location to use
        location_header = f'Location: http://{FILES_SERVER_HOST}:{FILES_SERVER_PORT}{path}\r\n'

        # organize the response as redirect format by the location
        response_data = to_html_format_Redirect(location_header)

        # send the response data back to the client
        client_connection.sendall(response_data)

        # close the client connection
        client_connection.close()


# to run all the code
if __name__ == '__main__':
    main_proxy()