import socket
import threading
import time
import json
import queue
import random
import string

clinet = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
clinet.bind(("localhost",  5604 + random.randint(1, 1000)))
name = input("UserName: ")


def receive_message():
    while True:
        try:
            message, _ = clinet.recvfrom(1024)
            print(message.decode())
        except:
            print("Error receiving message")
            pass


t1 = threading.Thread(target=receive_message)
t1.start()

clinet.sendto(f"SIGNUP_TAG:{name}".encode(), ("localhost", 5604))

while True:
    message = input("")
    if message == "exit":
        clinet.sendto(f"{name} left!".encode(), ("localhost", 5604))
        exit()
    else:
        clinet.sendto(f"{name}: {message}".encode(), ("localhost", 5604))
