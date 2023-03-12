import socket
from time import sleep
from helper import check_domain

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('127.0.0.1', 53)
BUFFER = 512
sock.settimeout(5)

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
            data, server = sock.recvfrom(BUFFER)
            ip_add = data.decode('utf-8')
            print(f"Found ip for {domain} The ip is  {ip_add}")
        except socket.timeout:
            print("NO IP FOUND FOR THIS DOMAIN, CHECK THE DOMAIN AND TRY AGAIN")

    sock.close()

if __name__ == '__main__':
    client_request()





