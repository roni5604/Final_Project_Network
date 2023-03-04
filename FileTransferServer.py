import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
machine = socket.gethostname()
port = 9999

server.bind((machine, port))
server.listen()


def sender():
    print(f"[{machine} waiting for the connection from the client")
    while True:
        client, address = server.accept()
        print("client connected and sending the file now")

        file = open("roni.txt")
        data = file.read(1024)
        while True:
            if data:
                print("sending data")
                client.send(data)
                data = file.read(1024)
                print("data send successfully")
                break

            else:
                print("failed to sent data")
                break

sender()