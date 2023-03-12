
import socket
from time import sleep

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('127.0.0.1', 53)
BUFF = 512
sock.settimeout(5)

def check_domain(domain):
    domain_split = domain.split(".")
    if len(domain_split) < 2:
        return False
    if domain.startswith("www.") is False:
        return False
    if domain.endswith(".com") is True:
        return True
    if domain.endswith(".co.il") is True:
        return True
    if domain.endswith(".gov.il") is True:
        return True
    if domain.endswith(".net") is True:
        return True
    if domain.endswith(".org") is True:
        return True
    if domain.endswith(".edu") is True:
        return True
    return False

def client_request():
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
            data, server = sock.recvfrom(BUFF)
            ip_add = data.decode('utf-8')
            print(f"Found ip for {domain} The ip is  {ip_add}")
        except socket.timeout:
            print("NO IP FOUND FOR THIS DOMAIN, CHECK THE DOMAIN AND TRY AGAIN")

    sock.close()

if __name__ == '__main__':
    client_request()





