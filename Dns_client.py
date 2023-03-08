import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('127.0.0.1', 53)
BUFF = 512
msg = "www.google.com"
try:
    domain = input("enter the domain you want: ")
    msgg = domain.encode('utf-8')
    print(f"SENDING DNS QUERY FOR {domain}")
    sock.sendto(msgg,server_address)

    data, server = sock.recvfrom(BUFF)
    ip_add = data.decode('utf-8')
    print(f"THE IP FOR {domain} is {ip_add}")
except Exception as e:
    print("ERROR: {e}")
sock.close()

#
#
# sock.connect(("127.0.0.1",53))
# sock.sendto(msg.encode(), server_address)
#
# data, server = sock.recvfrom(512)
# print("received message")
# sock.close()