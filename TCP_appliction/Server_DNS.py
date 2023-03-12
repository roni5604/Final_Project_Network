import socket
from _socket import gethostbyname

# handler for the dns request
def handle_dns_request(data, addr, sock):
    print("Received packet from: ", addr)
    print("Packet data: ", data.decode())
    print("")
    try:
        # get the ip address from the domain name
        response = gethostbyname(data.decode())
    except socket.gaierror:
        response = None

    if response is None:
        print(f"Not found ip for this address {data.decode()}")
    else:
        # if the ip is found send it to the client
        sock.sendto(response.encode(), addr)

# run the dns server
def run_dns_server():
    # create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # bind the socket to the port of the dns server
    sock.bind(('127.0.0.1', 53))
    while True:
        # receive the data from the client
        data, addr = sock.recvfrom(1024)
        # handle the dns request
        handle_dns_request(data, addr, sock)

# main function to the dns server
if __name__ == '__main__':
    print("DNS Server is running...")
    run_dns_server()
