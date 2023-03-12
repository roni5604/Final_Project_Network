import socket
from consts import PROXY_HOST, PROXY_PORT


# client function to test the server and proxy
def main_client_test():
    # create a TCP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connect to the proxy server
    client_socket.connect((PROXY_HOST, PROXY_PORT))

    # send a GET request for the file "test.txt"
    request_data = b'GET /TCP_appliction/test.txt HTTP/1.1\r\nHost: localhost:5604\r\n\r\n'
    client_socket.sendall(request_data)

    # receive the response data from the proxy server
    response_data = b''
    while True:
        # until not get the data not continue to next line
        data = client_socket.recv(1024)
        if not data:
            break
        # adding the data to one big message
        response_data += data

    # print the response data
    print(response_data.decode())

    # close the client socket
    client_socket.close()

# main running
if __name__ == '__main__':
    main_client_test()
