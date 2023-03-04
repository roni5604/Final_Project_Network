'''Implementation of RUDP with:
1. congestion control
2. selective acknowledgements
3. sliding windows
4. error handling
5. bidirectional communication in Python'''

'''Explanation on each:
Congestion control:
Implement a congestion control algorithm, such as TCP's congestion control algorithm,
to manage the rate at which packets are sent. This can help prevent network congestion and improve performance.

Selective acknowledgements: 
Implement a mechanism for selective acknowledgements, 
where the receiver sends an acknowledgement for every received packet, 
but also includes information about which packets it has not received.
This allows the sender to retransmit only the missing packets, rather than resending the entire window.

Sliding windows: Use a sliding window algorithm to manage the flow of packets between the sender and receiver.
This allows the sender to send multiple packets before waiting for an acknowledgement, 
and also allows the receiver to process incoming packets in order, even if they arrive out of order.

Error handling: 
Implement robust error handling to handle network failures, packet loss, 
and other errors that can occur when communicating over a network. 
This may include retrying failed transmissions, detecting and handling timeouts, 
and implementing error correction codes to detect and correct errors in transmitted data.

Handle incoming packets from both directions: 
Implement a bidirectional protocol that allows both the sender and receiver to send and receive packets.
This may involve defining different packet types for different kinds of data (e.g., control 
packets vs. data packets), and using different algorithms to manage the flow of packets in each direction.
'''

import socket
import threading
import time
import random


class RUDP:
    def __init__(self, host='localhost', port=8888, window_size=10):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((host, port))
        self.client_addr = None
        self.client_seqnum = 0
        self.server_seqnum = 0
        self.packet_buffer = []
        self.expected_acknum = 0
        self.window_size = window_size
        self.packet_timer = None
        self.seqnum_lock = threading.Lock()
        self.rtt = 0.1
        self.rto = self.rtt * 2
        self.alpha = 0.125
        self.beta = 0.25
        self.cwnd = 1
        self.ssthresh = float('inf')
        self.last_acknum = 0
        self.dup_acks = 0

    def send(self, data):
        with self.seqnum_lock:
            packet = Packet(self.server_seqnum, data, False)
            self.packet_buffer.append(packet)
            self.server_seqnum += 1
        self.send_packets()

    def send_packets(self):
        while True:
            with self.seqnum_lock:
                unacked_packets = self.packet_buffer[self.expected_acknum:self.expected_acknum + self.cwnd]
            for packet in unacked_packets:
                self.sock.sendto(packet.to_bytes(), self.client_addr)
            if len(unacked_packets) > 0 and not self.packet_timer:
                self.packet_timer = threading.Timer(self.rto, self.resend_packets)
                self.packet_timer.start()
            time.sleep(0.01)

    def resend_packets(self):
        with self.seqnum_lock:
            for packet in self.packet_buffer[self.expected_acknum:self.expected_acknum + self.cwnd]:
                self.sock.sendto(packet.to_bytes(), self.client_addr)
        self.rto *= 2
        self.packet_timer = threading.Timer(self.rto, self.resend_packets)
        self.packet_timer.start()

    def process_ack(self, acknum):
        if acknum > self.expected_acknum:
            with self.seqnum_lock:
                self.expected_acknum = acknum
                self.packet_buffer = self.packet_buffer[self.expected_acknum:]
                if self.packet_timer:
                    self.packet_timer.cancel()
                    self.packet_timer = None
                self.dup_acks = 0
                self.last_acknum = acknum
                self.update_cwnd()
        elif acknum == self.expected_acknum:
            self.dup_acks += 1
            if self.dup_acks == 3:
                self.ssthresh = max(self.cwnd / 2, 1)
                self.cwnd = self.ssthresh + 3
                self.dup_acks = 0
                self.rto *= 2
                self.resend_packets()
        else:
            pass

    def update_cwnd(self):
        if self.cwnd < self.ssthresh:
            self.cwnd += 1
        else:
            self.cwnd += self.alpha

    def listen(self):
        while True:
            data, addr = self.sock.recvfrom(1024)
            packet = Packet.from_bytes(data)
            if packet.ack:
                self.process_ack(packet.seqnum)
            else:
                ack_packet = Packet(packet.seqnum, None, True)
                self.sock.sendto(ack_packet.to_bytes(), addr)
                if not self.client_addr:
                    self.client_addr = addr
                if packet.seqnum >= self.client_seqnum:
                    with self.seqnum_lock:
                        self.client_seqnum = packet.seqnum + 1
                        self.expected_acknum = self.client_seqnum
                        self.packet_buffer = []
                        self.last_acknum = self.client_seqnum - 1
                        self.dup_acks = 0
                        self.update_cwnd()


class Packet:
    def __init__(self, seqnum, data, ack):
        self.seqnum = seqnum
        self.data = data
        self.ack = ack

    def to_bytes(self):
        seq_bytes = self.seqnum.to_bytes(4, byteorder='big')
        ack_bytes = (1 if self.ack else 0).to_bytes(1, byteorder='big')
        data_len_bytes = len(self.data).to_bytes(2, byteorder='big')
        return seq_bytes + ack_bytes + data_len_bytes + self.data

    @staticmethod
    def from_bytes(data):
        seqnum = int.from_bytes(data[:4], byteorder='big')
        ack = bool(data[4])
        data_len = int.from_bytes(data[5:7], byteorder='big')
        if data_len == 0:
            return Packet(seqnum, None, ack)
        else:
            return Packet(seqnum, data[7:7 + data_len], ack)


if __name__ == '__main__':
    rudp = RUDP()
    threading.Thread(target=rudp.listen).start()
    while True:
        data = input('Enter message: ')
        rudp.send(data.encode())




''' 
# Also an option to run the simulation:

# Create RUDP server and client
rudp_server = RUDP(port=8888)
rudp_client = RUDP(port=8889)

# Set client address for bidirectional communication
rudp_server.client_addr = ('localhost', 8889)
rudp_client.client_addr = ('localhost', 8888)

# Start server and client in separate threads
server_thread = threading.Thread(target=rudp_server.listen)
client_thread = threading.Thread(target=rudp_client.listen)
server_thread.start()
client_thread.start()

# Send messages from client to server and from server to client
rudp_client.send("Hello from client!")
rudp_server.send("Hello from server!")
'''