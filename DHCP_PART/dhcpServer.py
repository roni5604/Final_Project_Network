# make your own dhcp server in python
import binascii
import enum
import socket
import threading
import time
import json
import queue
import random
import string
from telnetlib import IP

from scapy.all import *
from scapy.layers.dhcp import DHCP, BOOTP
from scapy.layers.inet import UDP
from scapy.layers.l2 import Ether

SRC = "0.0.0.0"

ADDRESS = "255.255.255.255"
subnet_mask = "255.255.255.0"       # Subnet mask for the network
lease_time = 60
server_mac="3c:06:30:3b:a7:99"
server_ip="192.168.3.17"

# dhcp server port number is 67
PORT = 67
# dhcp client port number is 68
clientPort = 68

# list of all the clients
clients = []

# list of all the leases
leases = []

bootRequest = 1
bootReply = 2
Discover = 1
Offer = 2
Request = 3
Ack = 5
Nak = 6

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)


class DHCPOffer:
    def __init__(self, xid, mac, ip) -> object:
        self.TransactionID = hex(xid)
        self.MacInBytes = mac.replace(':', '')
        self.IP = ip
        if self.IP in leases:
            while self.IP in leases:
                self.IP = ("192.168.3." + random.randint(17, 254))
        leases.append(self.IP)

    def DHCP_Offer(self):
        self.op = '\x02'
        self.htype = '\x01'
        self.hlen = '\x06'
        self.hops = '\x00'
        self.xid = self.TransactionID
        self.secs = '\x00\x00'
        self.flags = '\x80\x00'
        self.ciaddr = '\x00\x00\x00\x00'
        self.yiaddr = self.IP
        self.siaddr = '\x00\x00\x00\x00'
        self.giaddr = '\x00\x00\x00\x00'
        self.chaddr = self.MacInBytes
        self.chwpadding = '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        self.sname = '\x00' * 64
        self.file = '\x00' * 128
        self.magic_cookie = '\x63\x82\x53\x63'
        self.msg_type = '\x35\x01\x02'
        self.client_id = '\x3d\x07\x01' + self.MacInBytes
        self.param_req_list = '\x37\x03\x03\x01\x06'
        self.end = '\xff'
        pkt2 = self.op + self.htype + self.hlen + self.hops + str(
            self.xid) + self.secs + self.flags + self.ciaddr + self.yiaddr + self.siaddr + self.giaddr + self.chaddr + self.chwpadding + self.sname + self.file + self.magic_cookie + self.msg_type + self.client_id + self.param_req_list + self.end

        return pkt2



class DHCPAck:
    def __init__(self, xid, mac, ip):
        self.TransactionID = hex(xid)
        self.MacInBytes = mac.replace(':', '')
        self.IP = ip

    def DHCP_Ack(self):
        if self.IP in leases:
            self.op = '\x02'
            self.htype = '\x01'
            self.hlen = '\x06'
            self.hops = '\x00'
            self.xid = self.TransactionID
            self.secs = '\x00\x00'
            self.flags = '\x80\x00'
            self.ciaddr = '\x00\x00\x00\x00'
            self.yiaddr = self.IP
            self.siaddr = '\x00\x00\x00\x00'
            self.giaddr = '\x00\x00\x00\x00'
            self.chaddr = self.MacInBytes
            self.chwpadding = '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
            self.sname = '\x00' * 64
            self.file = '\x00' * 128
            self.magic_cookie = '\x63\x82\x53\x63'
            self.msg_type = '\x35\x01\x05'
            self.client_id = '\x3d\x07\x01' + self.MacInBytes
            self.param_req_list = '\x37\x03\x03\x01\x06'
            self.end = '\xff'
            pkt2 = self.op + self.htype + self.hlen + self.hops + str(
                self.xid) + self.secs + self.flags + self.ciaddr + self.yiaddr + self.siaddr + self.giaddr + self.chaddr + self.chwpadding + self.sname + self.file + self.magic_cookie + self.msg_type + self.client_id + self.param_req_list + self.end
            return pkt2

def packetHandler(pkt):
    if pkt[DHCP].options[0][1] == 1:
        print("Discover")
        # Extract the MAC address of the client
        client_mac = pkt[Ether].src

        pktOfferObject = DHCPOffer(pkt[BOOTP].xid, client_mac, ("192.168.3." + str(random.randint(17, 254))))
        pktOffer = pktOfferObject.DHCP_Offer()

        yiaddr_offer = pktOfferObject.IP
        offer1 = Ether(src=server_mac, dst=client_mac) \
                 / IP(src=server_ip, dst="0.0.0.0") \
                 / UDP(sport=67, dport=68) \
                 / BOOTP(op=2, yiaddr=yiaddr_offer, siaddr=server_ip, chaddr=client_mac) \
                 / DHCP(pktOffer)
        sendp(offer1, iface="en0", verbose=0)
    elif pkt[DHCP].options[0][1] == 3:
        print("Request")
        client_mac = pkt[Ether].src
        yiaddr_ipdst = pkt[IP].src
        ciadder_ipdst = pkt[BOOTP].ciaddr
        pktAck = DHCPAck(pkt[BOOTP].xid, client_mac, pkt[BOOTP].yiaddr).DHCP_Ack()
        yiaddr_ack= pkt[BOOTP].yiaddr
        ack1 = Ether(src=server_mac, dst=client_mac) \
               / IP(src=server_ip, dst=ciadder_ipdst) \
                / UDP(sport=67, dport=68) \
                / BOOTP(op=2, yiaddr=yiaddr_ack, siaddr=server_ip, chaddr=client_mac) \
                / DHCP(pktAck)
        sendp(ack1, iface="en0", verbose=0)


if __name__ == '__main__':
    offers = sniff(filter="udp and (port 67 or 68)", prn=packetHandler)


