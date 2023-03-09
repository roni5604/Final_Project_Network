import socket
import threading
import time
import json
import queue
import random
import string
import os

HOST = '127.0.0.1'
PORT = 5604


def handle_client_request(resource, client_socket):
    url = resource
    if url != "/":
        pass
    else:
        url = 'LecturesWebPage.html'

    filename = os.path.basename(url)
    print
    url
    # TO DO: check if URL had been redirected, not available or other error code. For example:v
    if not os.path.exists(url) and os.path.exists("uploads/" + filename):
        http_header = "HTTP/1.0 302 FOUND\nLocation: /uploads/" + filename + "\n"
    elif not os.path.exists(url) and os.path.exists("js/" + filename):
        http_header = "HTTP/1.0 302 FOUND\nLocation: /js/" + filename + "\n"
    elif not os.path.exists(url) and os.path.exists("imges/" + filename):
        http_header = "HTTP/1.0 302 FOUND\nLocation: imges/" + filename + "\n"
    elif not os.path.exists(url) and os.path.exists("css/" + filename):
        http_header = "HTTP/1.0 302 FOUND\nLocation: /css/" + filename + "\n"

    else:
        pass
        # TO DO: send 302 redirection responsev

    # TO DO: extract requested file tupe from URL (html, jpg etc)v
    if os.path.exists("") or os.path.exists("LecturesWebPage.html"):
        http_header = "HTTP/1.0 200 OK\nContent-Type: text/html; charset=utf-8\n"
    elif os.path.exists("js/"):
        http_header = "HTTP/1.0 200 OK\nContent-Type: text/javascript; charset=UTF-8\n"
    elif os.path.exists("imgs/"):
        http_header = "HTTP/1.0 200 OK\nContent-Type: image/jpeg\n"
    elif os.path.exists("css/"):
        http_header = "HTTP/1.0 200 OK\nContent-Type: text/css\n"
    else:
        http_header = "HTTP 404 NOT FOUND\n"
    # TO DO: handle all other headersv
    # TO DO: read the data from the file
    data = get_file_data(url)
    http_response = http_header + data
    client_socket.send(http_response)


def get_file_data(filename):
    f = open(r"/Users/michaeli/PycharmProjects/Final_Project_Network/LecturesWebPage.html")
    return f.read()


def validate_http_request(resource):
    new_resource = resource.split(" ")
    command = new_resource[0]
    if command == "GET":
        return True, new_resource[1]
    else:
        return False, ""



def handle_client(client_socket, client_address):
    print('Client connected: %s:%s' % client_address)
    fin = open(r'LecturesWebPage.html')
    content = fin.read()
    # Send HTTP response
    response = 'HTTP/1.0 200 OK\n\n' + content
    client_socket.sendall(response.encode('utf-8'))
    while True:
        client_request = client_socket.recv(1024)
        valid_http, resource = validate_http_request(client_request)
        if valid_http:
            print ('Got a valid HTTP request')
            handle_client_request(resource, client_socket)
        else:
            print ('Error: Not a valid HTTP request')
            break
    print ('Closing connection')
    client_socket.close()


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print('Listening on port %s ...' % PORT)
    print('connect to http://%s:%s' % (HOST, PORT))
    while True:
        client_connection, client_address = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_connection, client_address))
        client_thread.start()


if __name__ == '__main__':
    main()
