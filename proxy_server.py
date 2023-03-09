import socket
import sys
import threading
from _dummy_thread import start_new_thread

from twisted.python.compat import raw_input

class ProxyServer:
    def __init__(self, listen_port, num_connections, buffer_size):
        self.listen_port = listen_port
        self.num_connections = num_connections
        self.buffer_size = buffer_size

    def proxy_server(self, webserver, port, conn, addr, data):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((webserver, port))
            sock.send(data)
            while 1:
                reply = sock.recv(self.buffer_size)
                if (len(reply) > 0):
                    conn.send(reply)
                    dar = float(len(reply))
                    dar = float(dar / 1024)
                    dar = "%.3s" % (str(dar))
                    dar = "%s KB" % (dar)
                    print("Request done: %s => %s <=" % (str(addr[0]), str(dar)))
                else:
                    break
            sock.close()
            conn.close()
        except socket.error as e:
            print("Error connecting to remote server: %s" % e)
            sock.close()
            conn.close()
            sys.exit(1)

    def conncetion_string(conn, data, addr):
        try:
            first_line = data.split('\n')[0]
            url = first_line.split(' ')[1]
            http_pos = url.find("://")
            if (http_pos == -1):
                temp = url
            else:
                temp = url[(http_pos + 3):]
            port_pos = temp.find(":")
            webserver_pos = temp.find("/")
            if webserver_pos == -1:
                webserver_pos = len(temp)
            webserver = ""
            port = -1
            if (port_pos == -1 or webserver_pos < port_pos):
                port = 80
                webserver = temp[:webserver_pos]
            else:
                port = int((temp[(port_pos + 1):])[:webserver_pos - port_pos - 1])
                webserver = temp[:port_pos]
            conn.proxy_server(webserver, port, conn, addr, data)
        except Exception as e:
            print(e)
            pass

    def start(self):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.bind(('', self.listen_port))
            sock.listen(self.num_connections)
            print("Proxy server started on port %d" % self.listen_port)
            print("server running on port %d" % self.listen_port)
        except socket.error as e:
            print("Error starting proxy server: %s" % e)
            sys.exit(1)
        while True:
            try:
                conn, addr = sock.accept()
                data = conn.recv(self.buffer_size)
                print("Received connection from %s" % addr[0])
                start_new_thread(self.conncetion_string, (conn, data , addr))
            except KeyboardInterrupt:
                print("Exiting...")
                sock.close()
                sys.exit(1)
        sock.close()




def main():
    try:
        listen_port = int(raw_input("Enter the port number to listen on: "))
    except KeyboardInterrupt:
        print("Exiting...")
        sys.exit(1)
    num_connections = 5
    buffer_size = 512

