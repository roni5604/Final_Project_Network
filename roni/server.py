from scapy.all import *
import random

from scapy.layers.dhcp import BOOTP, DHCP
from scapy.layers.inet import IP, UDP
from scapy.layers.l2 import Ether

# Define the IP range for DHCP to assign addresses from
ip_range = "192.168.0."!!!!!!!!!

# Define the MAC address of the server
mac = "00:11:22:33:44:66"!!!!!!!!!

etrenetType="en33"!!!!!!!!!!!!!!!

# Define the lease time for assigned IP addresses (in seconds)
lease_time = 3600

# Define the list of assigned IP addresses
assigned_ips = {}

# Define a function to generate a new IP address
def get_new_ip():
    new_ip = ip_range + str(random.randint(100, 200))!!!!!!!!!!!
    while new_ip in assigned_ips:
        new_ip = ip_range + str(random.randint(100, 200))!!!!!!!!!!!!!!!!!
    return new_ip

# Define a function to handle DHCP Discover messages
def handle_dhcp_discover(packet):
    # Extract the MAC address of the client
    mac = packet[Ether].src

    # Generate a new IP address for the client
    ip = get_new_ip()

    # Add the IP address to the list of assigned IPs
    assigned_ips[ip] = {"mac": mac, "lease_time": lease_time}

    # Create a DHCP Offer packet with the new IP address
    dhcp_offer = Ether(dst="ff:ff:ff:ff:ff:ff", src=mac)/ \
                 IP(src=ip_range+"1", dst="255.255.255.255")/ \
                 UDP(sport=67, dport=68)/ \
                 BOOTP(op=2, yiaddr=ip, siaddr=ip_range+"1", giaddr="0.0.0.0", xid=packet[BOOTP].xid)/ \
                 DHCP(options=[("message-type", "offer"),("server_id", ip_range+"1"),("subnet_mask", "255.255.255.0"),("lease_time", lease_time),("router", ip_range+"1"),"end"])

    # Send the DHCP Offer packet
    sendp(dhcp_offer, iface=etrenetType)!!!!!!!!!!!!!!!!

# Define a function to handle DHCP Request messages
def handle_dhcp_request(packet):
    # Extract the IP address requested by the client
    requested_ip = packet[BOOTP].ciaddr

    # Extract the MAC address of the client
    mac = packet[Ether].src

    # Check if the requested IP address is available and assigned to this client
    if requested_ip in assigned_ips and assigned_ips[requested_ip]["mac"] == mac:
        # Create a DHCP Ack packet with the assigned IP address
        dhcp_ack = Ether(dst="ff:ff:ff:ff:ff:ff", src=mac)/ \
                   IP(src=ip_range+"1", dst="255.255.255.255")/ \
                   UDP(sport=67, dport=68)/ \
                   BOOTP(op=2, yiaddr=requested_ip, siaddr=ip_range+"1", giaddr="0.0.0.0", xid=packet[BOOTP].xid)/ \
                   DHCP(options=[("message-type", "ack"),
                                  ("server_id", ip_range+"1"),
                                  ("subnet_mask", "255.255.255.0"),
                                  ("lease_time", assigned_ips[requested_ip]["lease_time"]),
                                  ("router", ip_range+"1"),
                                  "end"])

        # Send the DHCP Ack packet
        sendp(dhcp_ack, iface=etrenetType)

# Start sniffing for DHCP Discover and Request messages
sniff(filter="udp and (port 67 or port 68)", prn=lambda x: handle_dhcp_discover(x) if x[DHCP].options[0][1] == 1 else handle_dhcp_request(x), iface=etrenetType)

