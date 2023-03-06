import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
machine = socket.gethostname()
port = 9999

client.connect((machine, port))


def receiver():
    while True:
        print("receiving the file from the server")
        data = client.recv(1024)
        print("creating the file where to save the data")
        with open("NewSimpleFile.txt", "wb") as f:
            f.write(data)
            print("data has been received")
            break


receiver()
