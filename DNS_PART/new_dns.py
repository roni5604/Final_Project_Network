import socket

DNS_TABLE_com = {
    "www.google.com": "1.2.3.4",
    "www.yahoo.com": "5.6.7.8",
    "www.facebook.com": "5.5.5.5",
    "www.youtube.com": "8.7.6.7",
    "www.amazon.com": "4.3.2.4",
    "www.wikipedia.org": "2.3.4.8",
    "www.twitter.com": "6.8.9.8",
    "www.instagram.com": "4.5.4.5"
}
DNS_TABLE_org = {
    "www.wikipedia.org": "2.3.4.8",
}

DNS_TABLE_CO_IL = {
    "www.walla.co.il": "5.6.7.6",
    "www.ynet.co.il": "3.3.2.2",
    "www.mako.co.il": "2.4.5.6"
}

def get_ip_address(hostname):
    if hostname.endswith(".com"):
        if hostname in DNS_TABLE_com:
            return DNS_TABLE_com[hostname].encode()
    elif hostname in DNS_TABLE_org:
        return DNS_TABLE_org[hostname].encode()
    elif hostname in DNS_TABLE_CO_IL:
        return DNS_TABLE_CO_IL[hostname].encode()
    else:
        return None

def handle_dns_request(data, addr, sock):
    print(f"Received DNS request from {addr}")
    print("Received packet from: ", addr)
    print("Packet data: ", data.decode())
    print("Packet length: ", len(data))
    print("")
    response = get_ip_address(data.decode())
    if response is None:
        print(f"Could not find IP address for {data.decode()}")
    else:
        print(f"Found IP address {response} for {data.decode()}")
        sock.sendto(response, addr)






def run_dns_server():
    # create UDP socket and bind to port 53
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', 53))

    while True:
        # wait for incoming DNS request
        data, addr = sock.recvfrom(1024)
        # handle the DNS request
        handle_dns_request(data, addr, sock)

if __name__ == '__main__':
    run_dns_server()
