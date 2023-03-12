from scapy.all import *
import random
import threading
from scapy.layers.dhcp import BOOTP, DHCP
from scapy.layers.inet import IP, UDP
from scapy.layers.l2 import Ether

# define the IP range for DHCP to assign addresses from
ip_range = "192.168.75."

# define the MAC address of the server
mac = "00:0c:29:9b:51:47"

# define the interface to use, the loopback
ethernetType = "lo"

# define the lease time for assigned IP addresses (in seconds)
LEASE_TIME = 3600

# define the list of assigned IP addresses
assigned_ips = {}


# define a function to generate a new IP address
def get_new_ip():
    # generate a random number between 131 and 254 and add it to the IP range string
    new_ip = ip_range + str(random.randint(131, 254))
    # if the ip is in the assigned ips, repeat the process until a new IP address is generated
    while new_ip in assigned_ips:
        new_ip = ip_range + str(random.randint(131, 254))
    return new_ip


# define a function to handle DHCP Discover messages
def handle_dhcp_discover(packet):
    # extract the client mac address
    client_mac = packet[Ether].src

    # generate a new ip address to offer to the client
    ip_new = get_new_ip()

    # add the ip address to the list of assigned ips
    assigned_ips[ip_new] = {"mac": client_mac, "lease_time": LEASE_TIME}

    # create a DHCP offer packet with the new ip address to the client
    dhcp_offer = Ether(dst=client_mac) / \
                 IP(src=ip_range + "130", dst="255.255.255.255") / \
                 UDP(sport=67, dport=68) / \
                 BOOTP(op=2, yiaddr=ip_new, siaddr=ip_range + "130", giaddr="0.0.0.0", xid=packet[BOOTP].xid,
                       chaddr=client_mac) / \
                 DHCP(options=[("message-type", "offer"),
                               ("server_id", ip_range + "130"),
                               ("subnet_mask", "255.255.255.0"),
                               ("lease_time", LEASE_TIME),
                               ("router", ip_range + "2"),
                               "end"])

    print("server send offer")
    # Send the DHCP Offer packet
    time.sleep(1)
    # send the packet through the interface
    sendp(dhcp_offer, iface=ethernetType)


# handle DHCP request messages
def handle_dhcp_request(packet):
    # extract the requested ip address from the client
    requested_ip = packet[BOOTP].ciaddr

    # extract the client mac address
    client_mac = packet[Ether].src

    # check if the requested ip address is available and if it assigned to this client
    if requested_ip in assigned_ips and assigned_ips[requested_ip]["mac"] == client_mac:
        # create a DHCP ack packet with the assigned ip address
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
        # send the packet through the interface
        sendp(dhcp_ack, iface=ethernetType)
        print(assigned_ips)


# handle DHCP release messages
def packet_handler(packet):
    # check if the packet is a DHCP release message
    if DHCP in packet and packet[DHCP].options[0][1] == 1:
        handle_dhcp_discover(packet)
    # check if the packet is a DHCP request message
    elif DHCP in packet and packet[DHCP].options[0][1] == 3:
        handle_dhcp_request(packet)


# start sniffing for DHCP discover and request messages
sniff(filter="udp and (port 67 or port 68)", prn=packet_handler, iface=ethernetType)
