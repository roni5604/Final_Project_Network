import socket
import threading
import time


class RudpServer:
    def __init__(self, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('localhost', port))
        self.client_addr = None
        self.client_seqnum = None

    def listen(self):
        while True:
            data, self.client_addr = self.sock.recvfrom(1024)
            packet = Packet.from_bytes(data)
            if packet.seqnum == self.client_seqnum:
                self.client_seqnum += 1
                ack_packet = Packet(self.client_seqnum, None, True)
                self.sock.sendto(ack_packet.to_bytes(), self.client_addr)


class RudpClient:
    def __init__(self, server_addr, server_port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_addr = (server_addr, server_port)
        self.server_seqnum = 0
        self.seqnum_lock = threading.Lock()
        self.expected_acknum = 0
        self.packet_buffer = []
        self.window_size = 10
        self.packet_timer = None

    def send(self, data):
        with self.seqnum_lock:
            packet = Packet(self.server_seqnum, data, False)
            self.packet_buffer.append(packet)
            self.server_seqnum += 1
        self.send_packet(packet)

    def send_packet(self, packet):
        self.sock.sendto(packet.to_bytes(), self.server_addr)
        if not self.packet_timer:
            self.packet_timer = threading.Timer(0.1, self.resend_packets)
            self.packet_timer.start()

    def resend_packets(self):
        with self.seqnum_lock:
            for packet in self.packet_buffer:
                self.sock.sendto(packet.to_bytes(), self.server_addr)
        self.packet_timer = threading.Timer(0.1, self.resend_packets)
        self.packet_timer.start()

    def listen(self):
        while True:
            data, server_addr = self.sock.recvfrom(1024)
            packet = Packet.from_bytes(data)
            if packet.ack and packet.seqnum == self.expected_acknum:
                with self.seqnum_lock:
                    self.expected_acknum += 1
                    self.packet_buffer = [p for p in self.packet_buffer if p.seqnum > packet.seqnum]
                if self.packet_timer:
                    self.packet_timer.cancel()
                    self.packet_timer = None


class Packet:
    def __init__(self, seqnum, data, ack):
        self.seqnum = seqnum
        self.data = data
        self.ack = ack

    def to_bytes(self):
        return f"{self.seqnum},{int(self.ack)},{self.data}".encode()

    @staticmethod
    def from_bytes(data):
        parts = data.decode().split(",")
        seqnum = int(parts[0])
        ack = bool(int(parts[1]))
        data = parts[2] if len(parts) > 2 else None
        return Packet(seqnum, data, ack)


''' Here is how to run the simulation of RUDP: '''
# Start the server
server = RudpServer(8888)
server_thread = threading.Thread(target=server.listen)
server_thread.start()

# Start the client
client = RudpClient('localhost', 8888)
client_thread = threading.Thread(target=client.listen)
client_thread.start()

# Send a message
client.send("Hello, World!")
