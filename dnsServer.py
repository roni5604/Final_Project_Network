import socket


class DNS:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

        # # create a socket with UDP protocol
        # self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # create a socket with TCP protocol
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.socket.bind((self.ip, self.port))
        self.socket.listen(5)

    def start(self):
        while True:
            clientSocket, address = self.socket.accept()
            print(f"Connection established with {address}")
            print(clientSocket.recv(1024).decode())
            clientSocket.send(
                bytes("HTTP/1.1 200 OK \r\n\r\n<html><body><h1>Hello World from http server</h1></body></html>",
                      "utf-8"))
            clientSocket.close()
