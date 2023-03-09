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


import socket

BUFF = 512  # Buffer size


def recv_ip(domain):
    """
    Receives domain name and returns its IP
    if the domain name is invalid or didn't find IP returns None.
    :param domain: string of domain name
    :return: IP address according to the domain or None if invalid
    """
    try:
        ip = socket.gethostbyname(domain)
        return ip   # If the domain is good and has IP
    except socket.gaierror: # Get address info error
        return None


def dns_server(ip, port):
    """
    Receives requests for domain names and replies with its IP address
    :param ip: DNS Server IP
    :param port: DNS Server port
    :return: the IP of the specified domain name, if there is an error it returns the error
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((ip, port))
    print(f"DNS SERVER STARTED {ip},{port}")

    while True:
        data, addr = sock.recvfrom(BUFF)
        domain = data.decode()
        print(f"RECEIVED REQUEST FOR: {domain}")
        ip_add = recv_ip(domain)
        if ip_add is None:
            print(f"THERE IS NO IP FOR THAT DOMAIN!! {domain}")
            continue
        print("SENDING IP ADDRESS")
        sock.sendto(ip_add.encode(), addr)


dns_server("127.0.0.1", 53)