from scapy.all import *
import random
import threading
from scapy.layers.dhcp import BOOTP, DHCP
from scapy.layers.inet import IP, UDP
from scapy.layers.l2 import Ether

# Define the IP range for DHCP to assign addresses from
ip_range = "192.168.75."

# Define the MAC address of the server
mac = "00:0c:29:9b:51:47"

# Define
ethernetType= "lo"

# Define the lease time for assigned IP addresses (in seconds)
LEASE_TIME = 3600

# Define the list of assigned IP addresses
assigned_ips = {}


# Define a function to generate a new IP address
def get_new_ip():
    new_ip = ip_range + str(random.randint(131, 254))
    while new_ip in assigned_ips:
        new_ip = ip_range + str(random.randint(131, 254))
    return new_ip

# Define a function to handle DHCP Discover messages
def handle_dhcp_discover(packet):
    # Extract the MAC address of the client
    client_mac = packet[Ether].src

    # Generate a new IP address for the client
    ip_new = get_new_ip()

    # Add the IP address to the list of assigned IPs
    assigned_ips[ip_new] = {"mac": client_mac, "lease_time": LEASE_TIME}

    # Create a DHCP Offer packet with the new IP address
    dhcp_offer = Ether(dst=client_mac)/ \
                 IP(src=ip_range+"130", dst="255.255.255.255")/ \
                 UDP(sport=67, dport=68)/ \
                 BOOTP(op=2, yiaddr=ip_new, siaddr=ip_range+"130", giaddr="0.0.0.0", xid=packet[BOOTP].xid,chaddr=client_mac)/ \
                 DHCP(options=[("message-type", "offer"),
                               ("server_id", ip_range+"130"),
                               ("subnet_mask", "255.255.255.0"),
                               ("lease_time", LEASE_TIME),
                               ("router", ip_range + "2"),
                               "end"])

    print("server send offer")
    # Send the DHCP Offer packet
    time.sleep(1)
    sendp(dhcp_offer, iface=ethernetType)

# Define a function to handle DHCP Request messages
def handle_dhcp_request(packet):
    # Extract the IP address requested by the client
    requested_ip = packet[BOOTP].ciaddr

    # Extract the MAC address of the client
    client_mac = packet[Ether].src

    # Check if the requested IP address is available and assigned to this client
    if requested_ip in assigned_ips and assigned_ips[requested_ip]["mac"] == client_mac:
        # Create a DHCP Ack packet with the assigned IP address
        dhcp_ack = Ether(dst=client_mac) / \
                   IP(src=ip_range + "130", dst="255.255.255.255") / \
                   UDP(sport=67, dport=68) / \
                   BOOTP(op=2, yiaddr=requested_ip, siaddr=ip_range + "130", giaddr="0.0.0.0", xid=packet[BOOTP].xid,
                         chaddr=client_mac) / \
                   DHCP(options=[("message-type", "ack"),
                                 ("server_id", ip_range + "130"),
                                 ("subnet_mask", "255.255.255.0"),
                                 ("lease_time", assigned_ips[requested_ip]["lease_time"]),
                                 ("router", ip_range + "2"),
                                 "end"])

        print("server send ack")

        # Send the DHCP Ack packet
        time.sleep(1)
        sendp(dhcp_ack, iface=ethernetType)
        print(assigned_ips)


def packet_handler(packet):
    if DHCP in packet and packet[DHCP].options[0][1] == 1:
        handle_dhcp_discover(packet)
    elif DHCP in packet and packet[DHCP].options[0][1] == 3:
        handle_dhcp_request(packet)



# Start sniffing for DHCP Discover and Request messages
sniff(filter="udp and (port 67 or port 68)", prn=packet_handler, iface=ethernetType)



