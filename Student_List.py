import socket
import sys
import os
import queue
import threading
import time
import scrapy
import http.server
import socketserver
import subprocess
import urllib.request
import urllib.parse
import urllib.error
import json

CACHE_POLICY = True  # whether to cache responses or not
# the maximum time that the response can be cached for (in seconds)
CACHE_CONTROL = 2 ** 16 - 1
#data_list =[int,tuple[string, string]]#int of kind of request, tuple of name and email
def get_data_list():
    with open('List.txt', 'r') as f:
        list_of_client = f.read().splitlines()


class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/list') and self.path != '/list':
             if self.path == '/list/Student_List':
                 self.send_response(200)
                 self.send_header('Content-type', 'text/html')
                 self.end_headers()
                 with open('/files/List.txt', 'rb') as f:
                     self.wfile.write(f.read())
                     self.wfile.write("<html><body><h1>Student List</h1></body></html>", 'utf-8')


    def do_POST(self):

        def process_request(request: api.CalculatorHeader) -> api.CalculatorHeader:
            '''
            Function which processes a CalculatorRequest and builds a CalculatorResponse.
            '''
            result, steps = None, []
            try:
                if request.is_request:
                    expr = api.data_to_expression(request)
                    result, steps = calculate(expr, steps)
                else:
                    raise TypeError("Received a response instead of a request")
            except Exception as e:
                return api.CalculatorHeader.from_error(e, api.CalculatorHeader.STATUS_CLIENT_ERROR, CACHE_POLICY,
                                                       CACHE_CONTROL)

            if request.show_steps:
                steps = [api.stringify(step, add_brackets=True) for step in steps]
            else:
                steps = []

            return api.CalculatorHeader.from_result(result, steps, CACHE_POLICY, CACHE_CONTROL)

        def server(host: str, port: int) -> None:
            # socket(socket.AF_INET, socket.SOCK_STREAM)
            # (1) AF_INET is the address family for IPv4 (Address Family)
            # (2) SOCK_STREAM is the socket type for TCP (Socket Type) - [SOCK_DGRAM is the socket type for UDP]
            # Note: context manager ('with' keyword) closes the socket when the block is exited
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
                # SO_REUSEADDR is a socket option that allows the socket to be bound to an address that is already in use.
                server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                # Prepare the server socket
                # * Fill in start (1)
                # Tell the server on which port to listen to
                # Ready to listen up to 3 requests
                server_socket.bind((host, port))
                server_socket.listen(3)
                # * Fill in end (1)

                threads = []
                print(f"Listening on {host}:{port}")

                while True:
                    try:
                        # Establish connection with client.
                        # * Fill in start (2)
                        # Getting the relevant socket and address to use the connection
                        client_socket, address = server_socket.accept()
                        # * Fill in end (2)

                        # Create a new thread to handle the client request
                        thread = threading.Thread(target=client_handler, args=(client_socket, address))
                        thread.start()
                        threads.append(thread)
                    except KeyboardInterrupt:
                        print("Shutting down...")
                        break

                for thread in threads:  # Wait for all threads to finish
                    thread.join()

        def client_handler(client_socket: socket.socket, client_address: tuple[str, int]) -> None:
            '''
            Function which handles client requests
            '''
            client_addr = f"{client_address[0]}:{client_address[1]}"
            client_prefix = f"{{{client_addr}}}"
            with client_socket:  # closes the socket when the block is exited
                print(f"Conection established with {client_addr}")
                while True:
                    data = client_socket.recv(1024)
                    if not data:
                        break
                    try:
                        try:
                            if isNextRequest(data):
                                request = api.CalculatorHeader.unpack(data)
                            else:
                                break
                        except Exception as e:
                            raise api.CalculatorClientError(f'Error while unpacking request: {e}') from e

                        print(f"{client_prefix} Got request of length {len(data)} bytes")
                        response = process_request(request)
                        response = response.pack()
                        print(f"{client_prefix} Sending response of length {len(response)} bytes")
                        #  The server response send it back to the client
                        client_socket.sendall(response)
                    except Exception as e:
                        print(f"Unexpected server error: {e}")
                        client_socket.sendall(
                            api.CalculatorHeader.from_error(e, api.CalculatorHeader.STATUS_SERVER_ERROR, CACHE_POLICY,
                                                            CACHE_CONTROL).pack())
                    print(f"{client_prefix} Connection closed")
                client_socket.close()


    def do_PUT(self):
        if self.path == '/list/Student_List':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('List.txt', 'a') as f:
                f.write(self.data_list)
                f.write('\n')
                f.close()
    NextRequest = 1

    def isNextRequest(data):
        # change the global variable data to the next request
        global NextRequest
        if data[some_location] == NextRequest:
            NextRequest += 1
            return True
        return False






server= http.HTTPServer(('127.0.0.1', 5604), MyHttpRequestHandler)
server.serve_forever()

def main() -> None:
    arg_parser = argparse.ArgumentParser(description='SEND List Server.')
    arg_parser.add_argument('-p', '--port', type=int, default=api.DEFAULT_SERVER_PORT, help='The port to listen on.')
    arg_parser.add_argument('-H', '--host', type=str, default=api.DEFAULT_SERVER_HOST, help='The host to listen on.')
    args = arg_parser.parse_args()
    host = args.host
    port = args.port
    server(host, port)


if __name__ == '__main__':
    main()

