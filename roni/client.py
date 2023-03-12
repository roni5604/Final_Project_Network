from scapy.all import *
from scapy.layers.dhcp import BOOTP, DHCP
from scapy.layers.inet import IP, UDP
from scapy.layers.l2 import Ether

# Define the MAC address and IP address of the client
mac = "00:11:22:33:44:55"!!!!!!!!!!!!
ip = "0.0.0.0"!!!!!!!!!!!!

etrenetType="en33"!!!!!!!!!!!!!!!


# Create a DHCP Discover packet
dhcp_discover = Ether(dst="ff:ff:ff:ff:ff:ff", src=mac)/ \
                 IP(src="0.0.0.0", dst="255.255.255.255")/ \
                 UDP(sport=68, dport=67)/ \
                 BOOTP(chaddr=mac)/ \
                 DHCP(options=[("message-type", "discover"), "end"])

# Send the DHCP Discover packet and wait for the DHCP Offer
dhcp_offer = srp1(dhcp_discover, iface= etrenetType, timeout=10)!!!!!!!!!!!!!!!!!!

# Extract the offered IP address from the DHCP Offer
offered_ip = dhcp_offer[BOOTP].yiaddr

# Create a DHCP Request packet with the offered IP address
dhcp_request = Ether(dst="ff:ff:ff:ff:ff:ff", src=mac)/ \
                 IP(src="0.0.0.0", dst="255.255.255.255")/ \
                 UDP(sport=68, dport=67)/ \
                 BOOTP(chaddr=mac, ciaddr=offered_ip)/ \
                 DHCP(options=[("message-type", "request"),("requested_addr", offered_ip),"end"])

# Send the DHCP Request packet and wait for the DHCP Ack
dhcp_ack = srp1(dhcp_request, iface=etrenetType, timeout=10)!!!!!!!!!!!!!!

# Extract the assigned IP address from the DHCP Ack
assigned_ip = dhcp_ack[BOOTP].yiaddr

# Print the assigned IP address
print("Assigned IP address: " + assigned_ip)
