import socket
import pickle

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

items = []  # Empty list to store items

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print('Server is listening on', PORT)
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            received_items = pickle.loads(data)
            items.extend(received_items)  # Add received items to list
            if received_items == 'get_all_items':  # If client requests all items
                data = pickle.dumps(items)
                conn.sendall(data)
