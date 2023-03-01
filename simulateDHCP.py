from telnetlib import IP

from scapy.all import *
from scapy.layers.dhcp import BOOTP, DHCP
from scapy.layers.inet import UDP
from scapy.layers.l2 import Ether
from scapy.all import *

# Set up configurable parameters
mac_addr = get_if_raw_hwaddr(conf.iface)[1]  # MAC address of the DHCP client
iface = "en0"                  # Network interface to use
timeout = 5                     # Time to wait for DHCP offer and ACK packets

# Set up the DHCP discover packet
discover = Ether(dst="ff:ff:ff:ff:ff:ff")/IP(src="0.0.0.0", dst="255.255.255.255")/UDP(sport=68, dport=67)/BOOTP(chaddr=mac_addr)/DHCP(options=[("message-type", "discover"), "end"])

# Send the DHCP discover packet and wait for the DHCP offer packet
offer = srp1(discover, iface=iface, timeout=timeout)

if offer:
    # Extract the offered IP address from the DHCP offer packet
    offered_ip = offer[BOOTP].yiaddr

    # Set up the DHCP request packet
    request = Ether(dst="ff:ff:ff:ff:ff:ff")/IP(src="0.0.0.0", dst="255.255.255.255")/UDP(sport=68, dport=67)/BOOTP(chaddr=mac_addr, ciaddr="0.0.0.0")/DHCP(options=[("message-type", "request"), ("requested_addr", offered_ip), "end"])

    # Send the DHCP request packet and wait for the DHCP ACK packet
    ack = srp1(request, iface=iface, timeout=timeout)

    if ack:
        # Extract the assigned IP address from the DHCP ACK packet
        assigned_ip = ack[BOOTP].yiaddr

        # Print the assigned IP address
        print("Assigned IP address:", assigned_ip)
    else:
        print("No DHCP ACK packet received.")
else:
    print("No DHCP offer packet received.")
