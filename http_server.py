import socket
import threading
import time
import json
import queue
import random
import string

HOST = "localhost"
PORT = 5604

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind((HOST, PORT))
serverSocket.listen(5)
while True:
    clientSocket, address = serverSocket.accept()
    print(f"Connection established with {address}")
    print(clientSocket.recv(1024).decode())
    clientSocket.send(bytes("HTTP/1.1 200 OK \r\n\r\n<html><body><h1>Hello World from http server</h1></body></html>", "utf-8"))
    clientSocket.close()


