import socket
import time

port = 53  # DNS official port
ip = '127.0.0.1'  # IP of the computer loopback

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((ip, port))

while True:
    data, addr = sock.recvfrom(512)
    print(data)
