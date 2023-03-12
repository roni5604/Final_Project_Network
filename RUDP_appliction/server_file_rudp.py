from helpers import get_content_type
from consts import FILES_SERVER_HOST, FILES_SERVER_PORT
import socket
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main_tcp():
    # create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # bind the socket to a public host and port
    server_socket.bind((FILES_SERVER_HOST, FILES_SERVER_PORT))

    # listen for incoming connections

    print(f'Serving files on {FILES_SERVER_HOST}:{FILES_SERVER_PORT}...')

    while True:

        # accept incoming client connections
        while True:
            # get the request data in chunks



        request_data, client_address = server_socket.recvfrom(512)
        request_data = request_data.decode()
        # parse the request data
        request_lines = request_data.split('\r\n')
        request_line = request_lines[0]
        request_method, path, http_version = request_line.split()

        # construct the file path
        file_path = os.path.join(BASE_DIR, path[1:])
        # check if file exists and is readable
        if os.path.exists(file_path) and os.path.isfile(file_path) and os.access(file_path, os.R_OK):
            # read the file content
            with open(file_path, 'rb') as f:
                file_content = f.read()

            # construct the response data for a file download
            response_headers = [
                f'HTTP/1.1 200 OK',
                f'Content-Type: {get_content_type(file_path)}',
                f'Content-Length: {len(file_content)}',
                f'Content-Disposition: attachment; filename="{os.path.basename(file_path)}"',
                'Connection: close',
                '',
                ''
            ]
            response_data = '\r\n'.join(response_headers).encode() + file_content

        else:
            # construct the response data for a 404 Not Found error
            response_data = b'HTTP/1.1 404 Not Found\r\nContent-Length: 0\r\nConnection: close\r\n\r\n'




if __name__ == '__main__':
    main_tcp()
