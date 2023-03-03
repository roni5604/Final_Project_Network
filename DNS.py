import threading
import socket
import sys
import time
import random
import struct
import os
from dnslib import *
from scapy.all import *
from scapy.layers.dhcp import DHCP, BOOTP
from scapy.layers.inet import UDP
from scapy.layers.l2 import Ether


# Global Variables
global DNS_PORT
global DNS_IP

# DNS Server IP and Port
DNS_PORT = 53
DNS_IP = '127.0.0.1' # DNS Server IP

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((DNS_IP, DNS_PORT))


def getflags(flags):
    byte1 = bytes(flags[0:1])
    byte2 = bytes(flags[1:2])
    typeFlags = ''
    QereyResponse = '1'
    OPCODE=''
    for bit in range(1,5):
        OPCODE += str(ord(byte1) & (1 << bit))
    AA='1'
    TC='0'
    RD='0'
    RA='0'
    Z='000'
    RCODE='0000'
    typeFlags = int(QereyResponse + OPCODE + AA + TC + RD ,2).to_bytes(1, byteorder='big')+int(RA + Z + RCODE,2).to_bytes(1, byteorder='big')
    return typeFlags

def getQuestionDomain(data):
    state= 0
    expectedLength = 0
    domain = ''
    domainInparts = []
    x=0
    y=0
    for byte in data:
        if state == 1:
            domain += chr(byte)
            x += 1
            if x == expectedLength
                domainInparts.append(domain)
                domain = ''
                state = 0
                x=0
            if byte == 0:
                domainInparts.append(domain)
                break
        else:
            state = 1
            expectedLength = byte
        x+=1
        y+=1
    qustiontype = data[y+1:y+3]
    return (domainInparts,qustiontype)




def make_response(data):
    # Get the Transaction ID
    TransactionID = data[0:2]
    TID=''
    for byte in TransactionID:
        TID += (hex(byte)[2:])
    print("Transaction ID: ", TID)

    # Get the Flags
    Flags = getflags(data[2:4])
    print("Flags: ", Flags)

    # Get the Questions Count
    QDCOUNT = b'\x00\x01'
    print("Questions Count: ", QDCOUNT)

    # Get the Answer Count
    ANCOUNT = getQuestionDomain(data[12:])
    print("Answer Count: ", ANCOUNT)







def main():
    while True:
        data, addr = sock.recvfrom(512)
        print("Received packet from: ", addr)
        print("Packet data: ", data)
        print("Packet length: ", len(data))
        print("")
        response = make_response(data)
        sock.sendto(response, addr)





if __name__ == "__main__":
    main()
