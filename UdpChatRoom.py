import socket
import threading
import time
import json
import queue

Host = "localhost"
Port = 5604
message_queue = queue.Queue()
clinets = []

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((Host, Port))
server.listen(5)


def receive_message(client):
    while True:
        try:
            message, address = server.recvfrom(1024)
            message_queue.put((message, address))

        except:
            print("Error receiving message")
            pass


def broadcast_message():
    while True:
        while not message_queue.empty():
            message, address = message_queue.get()
            print(f"Message received from {address}: {message}")
            print(message.decode())
            if address not in clinets:
                clinets.append(address)
            for client in clinets:
                try:
                    if message.decode().startswith("SIGNUP_TAG:"):
                        name = message.decode()[message.decode().index(":") + 1:]
                        server.sendto(f"{name} joined!".encode(), client)
                    else:
                        server.sendto(message, client)
                except:
                    print(f"Error sending message to {client}")
                    clinets.remove(client)


t1 = threading.Thread(target=receive_message)
t2 = threading.Thread(target=broadcast_message)
t1.start()
t2.start()



