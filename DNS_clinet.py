import threading
import socket
import sys
import time
import random
import struct
import os
from dnslib import *

# Global Variables
global DNS_PORT
global DNS_IP

# DNS Server IP and Port
DNS_PORT = 53
DNS_IP = "" # DNS Server IP


class DNS_Client(threading.Thread):
    def __init__(self, port, ip):
        threading.Thread.__init__(self)
        self.port = port
        self.ip = ip
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.accept()

    def run(self):
        while True:
            data, addr = self.sock.recvfrom(1024)
            print("Received data from", addr)
            print("Data:", data)
            self.sock.sendto(data, addr)
def main():
    DNS_Client(DNS_PORT, DNS_IP).start()
