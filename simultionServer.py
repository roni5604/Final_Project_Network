from telnetlib import IP

from scapy.all import *
from scapy.layers.dhcp import DHCP, BOOTP
from scapy.layers.inet import UDP
from scapy.layers.l2 import Ether

# Set up the DHCP server parameters
server_mac = "00:11:22:33:44:55"    # MAC address of the server
server_ip = "192.168.1.1"           # IP address of the server
subnet_mask = "255.255.255.0"       # Subnet mask for the network
lease_time = 600                    # Lease time for the assigned IP address, in seconds
ip_pool = ["192.168.1.100", "192.168.1.200"]  # IP address pool to be assigned to clients

# Define the DHCP request handling function
def handle_dhcp_request(packet):
    # Check if the packet is a DHCP discover packet
    if DHCP in packet and packet[DHCP].options[0][1] == "discover":
        # Extract the MAC address of the client
        client_mac = packet[Ether].src

        # Choose an available IP address from the pool
        assigned_ip = None
        for ip in ip_pool:
            if ip not in assigned_ips:
                assigned_ip = ip
                assigned_ips.append(ip)
                break

        # If no IP address is available, return a NAK packet to the client
        if assigned_ip is None:
            nak = Ether(src=server_mac, dst=client_mac)/IP(src=server_ip, dst="255.255.255.255")/UDP(sport=67, dport=68)/BOOTP(op=2, yiaddr="0.0.0.0", siaddr=server_ip, chaddr=client_mac)/DHCP(options=[("message-type", "nak"), "end"])
            sendp(nak, iface="eth0")
        else:
            # Send a DHCP offer packet to the client
            offer = Ether(src=server_mac, dst=client_mac)/IP(src=server_ip, dst="255.255.255.255")/UDP(sport=67, dport=68)/BOOTP(op=2, yiaddr=assigned_ip, siaddr=server_ip, chaddr=client_mac)/DHCP(options=[("message-type", "offer"), ("subnet_mask", subnet_mask), ("lease_time", lease_time), ("server_id", server_ip), "end"])
            sendp(offer, iface="eth0")

    # Check if the packet is a DHCP request packet
    elif DHCP in packet and packet[DHCP].options[0][1] == "request":
        # Extract the MAC address and requested IP address of the client
        client_mac = packet[Ether].src
        requested_ip = packet[DHCP].options[1][1]

        # Send a DHCP ACK packet to the client with the assigned IP address
        ack = Ether(src=server_mac, dst=client_mac)/IP(src=server_ip, dst="255.255.255.255")/UDP(sport=67, dport=68)/BOOTP(op=2, yiaddr=requested_ip, siaddr=server_ip, chaddr=client_mac)/DHCP(options=[("message-type", "ack"), ("subnet_mask", subnet_mask), ("lease_time", lease_time), ("server_id", server_ip), "end"])
        sendp(ack, iface="eth0")

# Set up the list of assigned IP addresses
assigned_ips = []

# Start sniffing for DHCP requests
sniff(filter="udp and (port 67 or 68)", prn=handle_dhcp_request)
