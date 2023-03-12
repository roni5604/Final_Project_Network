import socket
from random import random

from scapy.layers.dhcp import DHCP, BOOTP
from scapy.layers.inet import IP, UDP
from scapy.layers.l2 import Ether
from scapy.sendrecv import srp1, sniff

from consts import PROXY_HOST, PROXY_PORT
from time import sleep
from helpers import check_domain

# Define the MAC address and IP address of the client
mac = "00:00:00:00:00:00"


def mac_to_bytes(mac_addr: str) -> bytes:
    """ Converts a MAC address string to bytes.
    """
    return int(mac_addr.replace(":", ""), 16).to_bytes(6, "big")


mac_in_bytes = mac_to_bytes(mac)
etrenetType = "lo"


# client function to test the server and proxy
def main_client_test():
    # create a TCP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connect to the proxy server
    client_socket.connect((PROXY_HOST, PROXY_PORT))

    # send a GET request for the file "test.txt"
    request_data = b'GET /TCP_appliction/test.txt HTTP/1.1\r\nHost: localhost:5604\r\n\r\n'
    client_socket.sendall(request_data)

    # receive the response data from the proxy server
    response_data = b''
    while True:
        # until not get the data not continue to next line
        data = client_socket.recv(1024)
        if not data:
            break
        # adding the data to one big message
        response_data += data

    # print the response data
    print(response_data.decode())

    # close the client socket
    client_socket.close()


def dns_client_request():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('127.0.0.1', 53)
    BUFFER = 512
    sock.settimeout(5)
    while True:
        try:
            print("")
            domain = input("Write an Address of the domaim you want to get (q to stop): ")
            if domain == "q":
                break
            if check_domain(domain) is False:
                print("ERROR IN DOMAIN, CHECK THE DOMAIN AND TRY AGAIN")
                continue
            msg = domain.encode('utf-8')
            print(f"Look for ip to  {domain}")
            sock.sendto(msg, server_address)
            sleep(1)
            data, server = sock.recvfrom(BUFFER)
            ip_add = data.decode('utf-8')
            print(f"Found ip for {domain} The ip is  {ip_add}")
        except socket.timeout:
            print("NO IP FOUND FOR THIS DOMAIN, CHECK THE DOMAIN AND TRY AGAIN")

    sock.close()


def client_DHCP():
    xid = random.randint(100, 100000)

    # Create a DHCP Discover packet
    from DHCP_PART.client import mac_in_bytes
    dhcp_discover = Ether(dst="ff:ff:ff:ff:ff:ff", src=mac) / \
                    IP(src="0.0.0.0", dst="255.255.255.255") / \
                    UDP(sport=68, dport=67) / \
                    BOOTP(op=1, chaddr=mac_in_bytes, xid=xid) / \
                    DHCP(options=[("message-type", "discover"), "end"])
    print("client send discover")
    # Send the DHCP Discover packet and wait for the DHCP Offer
    from DHCP_PART.client import etrenetType
    srp1(dhcp_discover, iface=etrenetType, timeout=0.5)
    sniff(filter="udp and (port 67 or port 68)", prn=handler_clienet, iface=etrenetType, stop_filter=lambda p: True)


def handler_clienet(packet):
    if DHCP in packet and packet[DHCP].options[0][1] == 2:
        # Extract the offered IP address from the DHCP Offer
        offered_ip = packet[BOOTP].yiaddr
        xid_requst = packet[BOOTP].xid

        # Create a DHCP Request packet with the offered IP address
        from DHCP_PART.client import mac_in_bytes
        dhcp_request = Ether(dst="ff:ff:ff:ff:ff:ff", src=mac) / \
                       IP(src="0.0.0.0", dst="255.255.255.255") / \
                       UDP(sport=68, dport=67) / \
                       BOOTP(op=1, chaddr=mac_in_bytes, ciaddr=offered_ip, xid=xid_requst, sname=b'', file=b'') / \
                       DHCP(options=[("message-type", "request"), ("requested_addr", offered_ip), "end"])

        print("client send request")

        # Send the DHCP Request packet and wait for the DHCP Ack
        srp1(dhcp_request, iface=etrenetType, timeout=0.5)


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
