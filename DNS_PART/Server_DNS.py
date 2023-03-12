import socket
from _socket import gethostbyname

def handle_dns_request(data, addr, sock):
    print("Received packet from: ", addr)
    print("Packet data: ", data.decode())
    print("")
    try:
        response = gethostbyname(data.decode())
    except socket.gaierror:
        response = None

    if response is None:
        print(f"Not found ip for this address {data.decode()}")
    else:
        sock.sendto(response.encode(), addr)
def run_dns_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', 53))
    while True:
        data, addr = sock.recvfrom(1024)
        handle_dns_request(data, addr, sock)

if __name__ == '__main__':
    print("DNS Server is running...")
    run_dns_server()
