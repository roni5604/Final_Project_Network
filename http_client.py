import socket
import threading
import time
import string
import random
import sys

serverHost = 'localhost'
serverPort = 5604
print("connecting to HTTP server on port %d" % serverPort)
httpClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
httpClient.connect((serverHost, serverPort))
httpClient.send(bytes("GET / HTTP/1.1\r\nHost: localhost\r\n\r\n".encode('utf-8')))
response = httpClient.recv(4096)
print("response: %s" % response.decode('utf-8'))

