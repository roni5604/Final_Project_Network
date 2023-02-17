import ipaddress
import socket
import struct

from Application import MongoClient

# just to add some imports just in case

import time
# from selenium import webdriver
import codecs
import sys
# import reload
import re
import fcntl
import os
import signal

# set up socket to listen for DHCP messages
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('0.0.0.0', 67))

# set up a database to store leases information
db = MongoClient().DHCP

# set up a dictionary to store leases information
leases = {}

# set up a dictionary to store the MAC address of the client
# and the IP address that the client has requested
requested_ips = {}

# define an ip address pool with the first 10 addresses to be used
# for static assignments
ip_address_pool = ipaddress.IPv4Network(' ')  # <-- we need to add our ip address pool here
ip_address_pool = list(ip_address_pool)
ip_address_pool = ip_address_pool[10:]



# define a function to handle the DHCP messages and respond appropriately
def handle_dhcp_message(message, client_address):
    message_type = message[0]
    if message_type == 1:
        handle_discover(message, client_address)
    elif message_type == 3:
        handle_request(message, client_address)
    elif message_type == 7:
        handle_release(message, client_address)
    else:
        print("Unknown DHCP message type", message_type)


# define a function to handle the DHCP discover message
def handle_discover(message, client_address):
    print("Handling DHCP discover message")
    # get the MAC address of the client
    mac_address = message[28:34]
    # check if the client has a lease
    if mac_address in leases:
        # if the client has a lease, send a DHCP offer message
        # with the IP address that the client has already been assigned
        send_dhcp_offer(client_address, leases[mac_address])
    else:
        # if the client does not have a lease, send a DHCP offer message
        # with a new IP address
        send_dhcp_offer(client_address, get_new_ip_address())


# define a function to handle the DHCP request message
def handle_request(message, client_address):
    print("Handling DHCP request message")
    # get the MAC address of the client
    mac_address = message[28:34]
    # get the IP address that the client has requested
    requested_ip_address = message[50:54]
    # check if the client has a lease
    if mac_address in leases:
        # if the client has a lease, check if the IP address that the client
        # has requested is the same as the IP address that the client has
        # already been assigned
        if requested_ip_address == leases[mac_address]:
            # if the IP address that the client has requested is the same as
            # the IP address that the client has already been assigned,
            # send a DHCP ack message
            send_dhcp_ack(client_address, leases[mac_address])
        else:
            # if the IP address that the client has requested is different
            # from the IP address that the client has already been assigned,
            # send a DHCP nak message
            send_dhcp_nak(client_address)
    else:
        # if the client does not have a lease, check if the IP address that
        # the client has requested is available
        if requested_ip_address in leases.values():
            # if the IP address that the client has requested is not available,
            # send a DHCP nak message
            send_dhcp_nak(client_address)
        else:
            # if the IP address that the client has requested is available,
            # send a DHCP ack message
            send_dhcp_ack(client_address, requested_ip_address)


# define a function to handle the DHCP release message
def handle_release(message, client_address):
    print("Handling DHCP release message")
    # get the MAC address of the client
    mac_address = message[28:34]
    # check if the client has a lease
    if mac_address in leases:
        # if the client has a lease, remove the lease from the dictionary
        del leases[mac_address]
        # remove the lease from the database
    elif mac_address in requested_ips:
        # if the client does not have a lease, but has requested an IP address,
        # remove the IP address from the dictionary
        del requested_ips[mac_address]
    else:
        # if the client does not have a lease and has not requested an IP address,
        # do nothing
        pass


# define a function to send a DHCP offer message
def send_dhcp_offer(client_address, ip_address):
    print("Sending DHCP offer message")
    # create a DHCP offer message
    message = bytearray()
    # set the message type to 2
    message.append(2)
    # set the hardware type to Ethernet
    message.append(1)
    # set the hardware address length to 6
    message.append(6)
    # set the hops to 0
    message.append(0)
    # set the transaction ID
    message.extend(b'\x12\x34\x56')
    # set the number of seconds elapsed to 0
    message.extend(b'\x00\x00')
    # set the flags
    message.extend(b'\x80\x00')
    # set the client IP address to
    message.extend(b'\x00\x00\x00\x00')

    ### SOME EXTRA CODE HERE ###

    # set the IP address to the IP address that the client has requested
    message.extend(ip_address)
    # set the server IP address to
    message.extend(b'\x00\x00\x00\x00')
    # set the gateway IP address to
    message.extend(b'\x00\x00\x00\x00')
    # set the client hardware address
    message.extend(b'\x00\x00\x00\x00\x00\x00')
    # set the server host name to
    message.extend(b'\x00' * 64)
    # set the boot file name to
    message.extend(b'\x00' * 128)
    # set the magic cookie
    message.extend(b'\x63\x82\x53\x63')
    # set the DHCP message type to 2
    message.extend(b'\x35\x01\x02')
    # set the subnet mask to
    message.extend(b'\x01\x04\xFF\xFF\xFF\x00')
    # set the router to
    message.extend(b'\x03\x04\x00\x00\x00\x00')
    # set the domain name server to
    message.extend(b'\x06\x04\x00\x00\x00\x00')
    # set the lease time to 86400 seconds
    message.extend(b'\x33\x04\x00\x01\x51\x80')
    # set the DHCP server identifier to
    message.extend(b'\x36\x04\x00\x00\x00\x00')
    # set the end option
    message.append(255)
    # send the DHCP offer message to the client
    s.sendto(message, client_address)


# define a function to send a DHCP ack message
def send_dhcp_ack(client_address, ip_address):
    print("Sending DHCP ack message")
    # create a DHCP ack message
    message = bytearray()
    # set the message type to 5
    message.append(5)
    # set the hardware type to Ethernet
    message.append(1)
    # set the hardware address length to 6
    message.append(6)
    # set the hops to 0
    message.append(0)
    # set the transaction ID
    message.extend(b'\x12\x34\x56')
    # set the number of seconds elapsed to 0
    message.extend(b'\x00\x00')
    # set the flags
    message.extend(b'\x80\x00')
    # set the client IP address to
    message.extend(b'\x00\x00\x00\x00')
    # set the IP address to the IP address that the client has requested
    message.extend(ip_address)
    # set the server IP address to
    message.extend(b'\x00\x00\x00\x00')
    # set the gateway IP address to
    message.extend(b'\x00\x00\x00\x00')
    # set the client hardware address
    message.extend(b'\x00\x00\x00\x00\x00\x00')
    # set the server host name to
    message.extend(b'\x00' * 64)
    # set the boot file name to
    message.extend(b'\x00' * 128)
    # set the magic cookie
    message.extend(b'\x63\x82\x53\x63')
    # set the DHCP message type to 5
    message.extend(b'\x35\x01\x05')
    # set the subnet mask to
    message.extend(b'\x01\x04\xFF\xFF\xFF\x00')
    # set the router to
    message.extend(b'\x03\x04\x00\x00\x00\x00')
    # set the domain name server to
    message.extend(b'\x06\x04\x00\x00\x00\x00')
    # set the lease time to 86400 seconds
    message.extend(b'\x33\x04\x00\x01\x51\x80')
    # set the DHCP server identifier to
    message.extend(b'\x36\x04\x00\x00\x00\x00')
    # set the end option
    message.append(255)
    # send the DHCP ack message to the client
    s.sendto(message, client_address)


# define a function to send a DHCP nak message
def send_dhcp_nak(client_address):
    print("Sending DHCP nak message")
    # create a DHCP nak message
    message = bytearray()
    # set the message type to 6
    message.append(6)
    # set the hardware type to Ethernet
    message.append(1)
    # set the hardware address length to 6
    message.append(6)
    # set the hops to 0
    message.append(0)
    # set the transaction ID
    message.extend(b'\x12\x34\x56')
    # set the number of seconds elapsed to 0
    message.extend(b'\x00\x00')
    # set the flags
    message.extend(b'\x80\x00')
    # set the client IP address to
    message.extend(b'\x00\x00\x00\x00')
    # set the IP address to
    message.extend(b'\x00\x00\x00\x00')
    # set the server IP address to
    message.extend(b'\x00\x00\x00\x00')
    # set the gateway IP address to
    message.extend(b'\x00\x00\x00\x00')
    # set the client hardware address
    message.extend(b'\x00\x00\x00\x00\x00\x00')
    # set the server host name to
    message.extend(b'\x00' * 64)
    # set the boot file name to
    message.extend(b'\x00' * 128)
    # set the magic cookie
    message.extend(b'\x63\x82\x53\x63')
    # set the DHCP message type to 6
    message.extend(b'\x35\x01\x06')
    # set the end option
    message.append(255)
    # send the DHCP nak message to the client
    s.sendto(message, client_address)


# create a function to get new IP address
# continue the "# if the client does not have a lease, send a DHCP offer message
#         # with a new IP address" section
# add the following code
def get_new_ip_address():
    # get the first IP address from the IP address pool
    ip_address = ip_address_pool[0]
    # remove the first IP address from the IP address pool
    ip_address_pool.remove(ip_address)
    # return the IP address
    return ip_address
