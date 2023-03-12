import socket
import random

from scapy.layers.dhcp import DHCP, BOOTP
from scapy.layers.inet import IP, UDP
from scapy.layers.l2 import Ether
from scapy.sendrecv import srp1, sniff

from consts import PROXY_HOST, PROXY_PORT
from time import sleep
from helpers import check_domain

# define the client mac address
mac = "00:00:00:00:00:00"

# convert the mac address to bytes
def mac_to_bytes(mac_addr: str) -> bytes:
    return int(mac_addr.replace(":", ""), 16).to_bytes(6, "big")

mac_in_bytes = mac_to_bytes(mac)
# define the interface to use, the loopback
ethernetType = "lo"


# client function to test the project
def main_client_test():
    # create a TCP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connect to the proxy server
    client_socket.connect((PROXY_HOST, PROXY_PORT))

    # send a GET request for the file "test.txt"
    request_data = b'GET /TCP_appliction/test.txt HTTP/1.1\r\nHost: localhost:5604\r\n\r\n'
    client_socket.sendall(request_data)

    # define a variable to store the response data
    response_data = b''
    # receive the response data from the proxy server
    while True:
        # recv the data from the socket, until not get the data not continue to next line
        data = client_socket.recv(1024)
        if not data:
            break
        # adding the data to one big message
        response_data += data

    # print the response data
    print(response_data.decode())

    # close the client socket
    client_socket.close()

# client dns request
def dns_client_request():
    # open UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # define the server address
    server_address = ('127.0.0.1', 53)
    BUFFER = 512 # define the buffer size
    sock.settimeout(5) # set the timeout to 5 seconds
    while True:
        try:
            print("")
            domain = input("Write an Address of the domaim you want to get (q to stop): ")
            if domain == "q":
                break
            if check_domain(domain) is False:
                print("ERROR IN DOMAIN, CHECK THE DOMAIN AND TRY AGAIN")
                continue
            # encode the domain to bytes
            msg = domain.encode('utf-8')
            print(f"Look for ip to  {domain}")
            # send the domain to the server
            sock.sendto(msg, server_address)
            sleep(1)
            # get the ip address from the server
            data, server = sock.recvfrom(BUFFER)
            ip_add = data.decode('utf-8')
            print(f"Found ip for {domain} The ip is  {ip_add}")
        except socket.timeout:
            print("NO IP FOUND FOR THIS DOMAIN, CHECK THE DOMAIN AND TRY AGAIN")

    sock.close()


# client dhcp request
def client_DHCP():
    # generate a random transaction ID
    xid = random.randint(100, 100000)

    # create a DHCP discover packet
    dhcp_discover = Ether(dst="ff:ff:ff:ff:ff:ff", src=mac) / \
                    IP(src="0.0.0.0", dst="255.255.255.255") / \
                    UDP(sport=68, dport=67) / \
                    BOOTP(op=1, chaddr=mac_in_bytes, xid=xid) / \
                    DHCP(options=[("message-type", "discover"), "end"])
    print("client send discover")
    # Send the DHCP Discover packet and wait for the DHCP Offer
    srp1(dhcp_discover, iface=ethernetType, timeout=0.5)
    # sniff the dhcp offer
    sniff(filter="udp and (port 67 or port 68)", prn=handler_client, iface=ethernetType, stop_filter=lambda p: True)


# handler for the dhcp offer
def handler_client(packet):
    # check if the packet is DHCP offer
    if DHCP in packet and packet[DHCP].options[0][1] == 2:
        # Extract the offered IP address from the DHCP Offer
        offered_ip = packet[BOOTP].yiaddr
        xid_request = packet[BOOTP].xid

        # Create a DHCP Request packet with the offered IP address
        dhcp_request = Ether(dst="ff:ff:ff:ff:ff:ff", src=mac) / \
                       IP(src="0.0.0.0", dst="255.255.255.255") / \
                       UDP(sport=68, dport=67) / \
                       BOOTP(op=1, chaddr=mac_in_bytes, ciaddr=offered_ip, xid=xid_request, sname=b'', file=b'') / \
                       DHCP(options=[("message-type", "request"), ("requested_addr", offered_ip), "end"])

        print("client send request")

        # Send the DHCP Request packet and wait for the DHCP Ack
        srp1(dhcp_request, iface=ethernetType, timeout=0.5)


# main function
if __name__ == '__main__':
    while True:
        what_to_do = input("What do you want to do? (1 for test the proxy, 2 for DNS request , 3 for DHCP request (q to stop)): ")
        if what_to_do == "q":
            break
        if what_to_do == "1":
            main_client_test()
        elif what_to_do == "2":
            dns_client_request()
        elif what_to_do == "3":
            client_DHCP()
