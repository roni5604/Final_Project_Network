from scapy.all import *
from scapy.layers.dhcp import BOOTP, DHCP
from scapy.layers.inet import IP, UDP
from scapy.layers.l2 import Ether


# Define the MAC address and IP address of the client
mac = "00:11:22:33:44:55"!!!!!!!!!!!!
ip = "0.0.0.0"!!!!!!!!!!!!

etrenetType="en33"!!!!!!!!!!!!!!!

def handler_clienet(packet):
    if DHCP in packet and packet[DHCP].options[0][1] == 2:
        # Extract the offered IP address from the DHCP Offer
        offered_ip = packet[BOOTP].yiaddr
        xid_requst = packet[BOOTP].xid

        # Create a DHCP Request packet with the offered IP address
        dhcp_request = Ether(dst="ff:ff:ff:ff:ff:ff", src=mac) / \
                       IP(src="0.0.0.0", dst="255.255.255.255") / \
                       UDP(sport=68, dport=67) / \
                       BOOTP(op=1, chaddr=mac_in_bytes, ciaddr=offered_ip, xid=xid_requst, sname=b'', file=b'') / \
                       DHCP(options=[("message-type", "request"), ("requested_addr", offered_ip), "end"])

        print("client send request")

        # Send the DHCP Request packet and wait for the DHCP Ack
        srp1(dhcp_request, iface=etrenetType, timeout=0.5)



sniff(filter="udp and (port 67 or port 68)", prn=handler_clienet, iface=etrenetType,stop_filter=lambda p: True)
