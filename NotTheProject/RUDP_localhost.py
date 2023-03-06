import socket
import threading
import time

class RUDP:
    def __init__(self, host='localhost', port=8888):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((host, port))
        self.client_addr = None
        self.client_seqnum = 0
        self.server_seqnum = 0
        self.packet_buffer = []
        self.expected_acknum = 0
        self.window_size = 10
        self.packet_timer = None
        self.seqnum_lock = threading.Lock()

    def send(self, data):
        with self.seqnum_lock:
            packet = Packet(self.server_seqnum, data, False)
            self.packet_buffer.append(packet)
            self.server_seqnum += 1
        self.send_packet(packet)

    def send_packet(self, packet):
        self.sock.sendto(packet.to_bytes(), self.client_addr)
        if not self.packet_timer:
            self.packet_timer = threading.Timer(0.1, self.resend_packets)
            self.packet_timer.start()

    def resend_packets(self):
        with self.seqnum_lock:
            for packet in self.packet_buffer:
                self.sock.sendto(packet.to_bytes(), self.client_addr)
        self.packet_timer = threading.Timer(0.1, self.resend_packets)
        self.packet_timer.start()

    def listen(self):
        while True:
            data, self.client_addr = self.sock.recvfrom(1024)
            packet = Packet.from_bytes(data)
            if packet.ack and packet.seqnum == self.expected_acknum:
                with self.seqnum_lock:
                    self.expected_acknum += 1
                    self.packet_buffer = [p for p in self.packet_buffer if p.seqnum > packet.seqnum]
                if self.packet_timer:
                    self.packet_timer.cancel()
                    self.packet_timer = None
            elif not packet.ack:
                ack_packet = Packet(packet.seqnum, None, True)
                self.sock.sendto(ack_packet.to_bytes(), self.client_addr)

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


''' Here is how to run the simulation on the localhost server: '''
# Start the server/client
rudp = RUDP()
rudp_thread = threading.Thread(target=rudp.listen)
rudp_thread.start()

# Send a message
rudp.send("Hello, World!")
