import socket

BUFFER = 512  # Buffer size


def recv_ip(domain):
    try:
        ip = socket.gethostbyname(domain)
        return ip  # If the domain is good and has IP
    except socket.gaierror:
        return None


def dns_server(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((ip, port))
    print(f"DNS SERVER STARTED {ip},{port}")

    while True:
        data, addr = sock.recvfrom(BUFFER)
        domain = data.decode()
        print(f"RECEIVED REQUEST FOR: {domain}")
        ip_add = recv_ip(domain)
        if ip_add is None:
            print(f"THERE IS NO IP FOR THAT DOMAIN!! {domain}")
            continue
        print("SENDING IP ADDRESS")
        sock.sendto(ip_add.encode(), addr)


dns_server('127.0.0.1', 53)
