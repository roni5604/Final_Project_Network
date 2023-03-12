import binascii
import socket
import threading
import time
import json
import queue
import random
import string
import struct
import enum
import scrapy
import requests
from scapy.all import *
from scapy.layers.dhcp import DHCP, BOOTP
from scapy.layers.inet import UDP, IP
from scapy.layers.l2 import Ether


# mac_addr = get_if_raw_hwaddr(conf.iface)[1]  # MAC address of the DHCP client


# DHCP server port number is 67
PORT = 67
# DHCP client port number is 68
clientPort = 68
timeout = 5

SRC = "0.0.0.0"
DEST = "255.255.255.255"

xid = random.randint(0, 0xFFFFFFF)
mac_addr = get_if_raw_hwaddr(conf.iface)[1]
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
clientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
clientSocket.bind((SRC, clientPort))


class DHCPDiscover:
    def __init__(self, xid, mac) -> object:
        self.TransactionID = hex(xid)
        self.MacInBytes = mac.replace(':', '')

    def DHCP(self):
        self.op = '\x01'
        self.htype = '\x01'
        self.hlen = '\x06'
        self.hops = '\x00'
        self.xid = self.TransactionID
        self.secs = '\x00\x00'
        self.flags = '\x80\x00'
        self.ciaddr = '\x00\x00\x00\x00'
        self.yiaddr = '\x00\x00\x00\x00'
        self.siaddr = '\x00\x00\x00\x00'
        self.giaddr = '\x00\x00\x00\x00'
        self.chaddr = self.MacInBytes
        self.chwpadding = '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        self.sname = '\x00' * 64
        self.file = '\x00' * 128
        self.magic_cookie = '\x63\x82\x53\x63'
        self.msg_type = '\x35\x01\x01'
        self.client_id = '\x3d\x07\x01' + self.MacInBytes
        self.param_req_list = '\x37\x03\x03\x01\x06'
        self.end = '\xff'
        pkt1 = self.op + self.htype + self.hlen + self.hops + str(
            self.xid) + self.secs + self.flags + self.ciaddr + self.yiaddr + self.siaddr + self.giaddr + self.chaddr + self.chwpadding + self.sname + self.file + self.magic_cookie + self.msg_type + self.client_id + self.param_req_list + self.end
        discover = Ether(dst="ff:ff:ff:ff:ff:ff") /\
                   IP(src="0.0.0.0", dst="255.255.255.255") / \
                   UDP(sport=68,dport=67) / BOOTP(chaddr=mac_addr) / \
                   DHCP(options=[("message-type", "discover"), "end"])
        return discover


class DHCPRequest:
    def __init__(self, xid, mac, yiaddro):
        self.TransactionID = hex(xid)
        self.MacInBytes = mac.replace(':', '')
        self.yiaddr = yiaddro

    def DHCP_request(self):
        self.op = '\x01'
        self.htype = '\x01'
        self.hlen = '\x06'
        self.hops = '\x00'
        self.xid = xid
        self.secs = '\x00\x00'
        self.flags = '\x80\x00'
        self.ciaddr = '\x00\x00\x00\x00'
        self.yiaddr = '\x00\x00\x00\x00'
        self.siaddr = '\x00\x00\x00\x00'
        self.giaddr = '\x00\x00\x00\x00'
        self.chaddr = self.MacInBytes + b'\x00' * (16 - len(self.MacInBytes))
        self.sname = '\x00' * 64
        self.file = '\x00' * 128
        self.magic_cookie = '\x63\x82\x53\x63'
        self.msg_type = '\x35\x01\x03'
        self.client_id = '\x3d\x07\x01' + self.MacInBytes
        self.req_addr = '\x32\x04' + socket.inet_aton(self.yiaddr)
        self.server_id = '\x36\x04'
        self.param_req_list = '\x37\x03\x03\x01\x06'
        self.end = '\xff'
        pkt2 = self.op + self.htype + self.hlen + self.hops + str(self.xid) + self.secs + self.flags + self.ciaddr + self.yiaddr + self.siaddr + self.giaddr + self.chaddr + self.chwpadding + self.sname + self.file + self.magic_cookie + self.msg_type + self.client_id + self.req_addr + self.server_id + self.param_req_list + self.end
        request = Ether(dst="ff:ff:ff:ff:ff:ff") / IP(src="0.0.0.0", dst="255.255.255.255") / UDP(sport=68,
                                                                                                  dport=67) / BOOTP(
            chaddr=mac_addr, ciaddr="0.0.0.0") / DHCP(pkt2)
        return request


if __name__ == "__main__":
    discoverObject = DHCPDiscover(xid, mac_addr)
    discover = discoverObject.DHCP()
    offer = srp1(discover, iface=mac_addr, timeout=timeout)
    if offer:
        # Extract the offered IP address from the DHCP offer packet
        offered_ip = offer[BOOTP].yiaddr

        # Set up the DHCP request packet
        request = DHCPRequest(xid, mac_addr, offered_ip)
        request.DHCP_request()

        # Send the DHCP request packet and wait for the DHCP ACK packet
        ack = srp1(request, iface=mac_addr, timeout=timeout)

        if ack:
            # Extract the assigned IP address from the DHCP ACK packet
            assigned_ip = ack[BOOTP].yiaddr

            # Print the assigned IP address
            print("Assigned IP address:", assigned_ip)
        else:
            print("No DHCP ACK packet received.")
    else:
        print("No DHCP offer packet received.")
