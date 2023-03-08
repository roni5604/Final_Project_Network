import json
import threading
import socket
import sys
import time
import random
import struct
import os
from dnslib import *
from scapy.all import *
import glob
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

def load_zone():
    zonefiles= glob.glob('zones/*.zone')
    print(zonefiles)
    jsonzone = {}
    for zone in zonefiles:
            with open(zone) as zoneData:
                data = json.load(zoneData)
                zonename = data['$origin']
                jsonzone[zonename] = data
    return jsonzone

zoneData = load_zone()

def getflags(flags):
    byte1 = bytes(flags[0:1])
    byte2 = bytes(flags[1:2])
    typeFlags = ''
    QereyResponse = '1'
    OPCODE=''
    for bit in range(1,5):
        OPCODE += str(ord(byte1) & (1 << bit))
    AA='1' # Authoritative Answer
    TC='0' # Truncation
    RD='0' # Recursion Desired
    RA='0' # Recursion Available
    Z='000' # Reserved
    RCODE='0000' # Response Code
    typeFlags = int(QereyResponse + OPCODE + AA + TC + RD ,2).to_bytes(1, byteorder='big')+int(RA + Z + RCODE,2).to_bytes(1, byteorder='big')
    return typeFlags




def getQuestionDomain(data):
    state= 0
    expectedLength = 0
    domainString = ''
    domainInparts = []
    x=0
    y=0
    for byte in data:
        if state == 1:
            if byte != 0:
                domainString += chr(byte)
            x += 1
            if x == expectedLength:
                domainInparts.append(domainString)
                domainString = ''
                state = 0
                x=0
            if byte == 0:
                domainInparts.append(domainString)
                break
        else:
            state = 1
            expectedLength = byte
        y+=1
    qustiontype = data[y:y+2]
    return (domainInparts,qustiontype)

def getZone(domain):
    global zoneData
    zone_name = '.'.join(domain)
    return zoneData[zone_name]

def getRecs(data):
    domain , qustiontype = getQuestionDomain(data)
    qt=''
    if qustiontype == b'\x00\x01':
        print("Qustion Type A")
        qt='a'
    zone= getZone(domain)
    return (zone[qt],qt,domain)

def buildqustion(domainName,rectype):
    qbytes = b''
    for part in domainName:
        length = len(part)
        qbytes += bytes([length])
        for char in part:
            qbytes = ord(char).to_bytes(1, byteorder='big')
    if rectype == 'a':
         qbytes += b'\x00\x01'
    qbytes += b'\x00\x01'
    print("qbytes is " + qbytes)
    return qbytes


def rectobytes(domainName,rectype,recTtl,recValue):
    rbytes = b'\xc0\x0c'
    if rectype == 'a':
        rbytes += b'\x00\x01'
    rbytes += b'\x00\x01'
    rbytes += int(recTtl).to_bytes(4, byteorder='big')
    if rectype == 'a':
        rbytes += b'\x00\x04'
    for part in recValue.split('.'):
        rbytes += bytes([int(part)])
    return rbytes



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
    ANCOUNT = len(getRecs(data[12:])[0]).to_bytes(2, byteorder='big')
    print("Answer Count: ", ANCOUNT)

    # Get the Name Server Count
    NSCOUNT = b'\x00\x00'

    # Get the Additional Count
    ARCOUNT = b'\x00\x00'

    dnshdr = TransactionID + Flags + QDCOUNT + ANCOUNT + NSCOUNT + ARCOUNT
    print("DNS Header: ", dnshdr)

    # Get the Dns body
    dnsbody = b''
    records ,rectype ,domainName = getRecs(data[12:])
    dnsQuestion = buildqustion(domainName,rectype)
    print("DNS Question: ", dnsQuestion)
    for record in records:
        dnsbody += rectobytes(domainName,rectype,record['ttl'],record['value'])
    print("DNS Body: ", dnsbody)
    return dnshdr + dnsQuestion + dnsbody





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
