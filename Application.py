from audioop import error
from socket import socket

from flask import Flask, redirect ,request
from pip._internal.exceptions import ConfigurationError

app = Flask(__name__)


@app.route('/',defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    query = request.query_string.decode('utf-8')
    redirect_url = f'https://www.google.com/search?q={query}'
    if query:
        redirect_url = f'{redirect_url}+site:{path}'
    return redirect(redirect_url , code=302)

if __name__ == '__main__':
    app.run(debug=True)

def client_handler(clinetAddress: tuple[str,int], clientPort: int, clientsocket: socket.socket,ServerAddress: tuple[str,int])
    client_prefix = clinetAddress[0]
    print(f"Client {client_prefix} connected")
    while True:
        try:
            data = clientsocket.recv(1024)
            if data:
                print(f"Data received from {client_prefix}: {data}")
                clientsocket.sendall(data)
            else:
                raise error('Client disconnected')
        except:
            print(f"Client {client_prefix} disconnected")
            break

def server(host: str, port: int):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen(5)
        while True:
            conn, addr = s.accept()
            with conn:
                client_handler(addr[0], addr[1], conn, (host, port))
    treads = []
    print("listening on port: ", port, " : ", host)
    while True:
        conn, addr = s.accept()
        tread= threading.Thread(target=client_handler, args=(addr[0], addr[1], conn, (host, port)))
        tread.start()
        treads.append(t)
        except KeyboardInterrupt:
            print("Shutting down server")
            for t in treads:
                t.join()
            break
        for tread in treads:
            tread.join()







def MongoReplicaSetClient(param, param1, document_class, tz_aware, connect, param2):
    param = param
    param1 = param1
    document_class = document_class
    tz_aware = tz_aware
    connect = connect
    param2 = param2
    return param, param1, document_class, tz_aware, connect, param2


def MongoClient(host=None, port=None, document_class=dict, tz_aware=False, connect=True, **kwargs):
    host = host or 'localhost'
    port = port or 27017
    if isinstance(port, str):
        port = int(port)
    if isinstance(host, str):
        host = [host]
    if isinstance(port, int):
        port = [port]
    if len(host) != len(port):
        raise ConfigurationError('host and port must have the same length')
    if len(host) == 1:
        return MongoReplicaSetClient(host[0], port[0], document_class, tz_aware, connect, **kwargs)
    return MongoReplicaSetClient(host, port, document_class, tz_aware, connect, **kwargs)



class Database:
    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["test"]
        self.db.authenticate("name", "password")
        self.db = self.client["test"]
        names = self.db.list_collection_names()
        if "test" not in names:
            self.db.create_collection("test")
        else:
            self.db.drop_collection("test")
            self.db.create_collection("test")


    def get_table(self, table_name):
        return self.db[table_name]



def main():
    print("start connecting to database")
    db = Database()
    print("connected to database")
    table = db.get_table("test")
    print("got table")
    table.insert({"name": "test", "age": 20})
    print("inserted")
    print(table.find_one(name="test"))
    print("found")
    table.update({"name": "test"}, {"name": "test", "age": 21})
    print("updated")
    print(table.find_one(name="test"))
    print("found")
    table.delete(name="test")
    print("deleted")
    print(table.find_one(name="test"))
    print("found")
    print("done")



