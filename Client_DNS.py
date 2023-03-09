
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('127.0.0.1', 53)
BUFF = 512
sock.settimeout(5)


def check_domain(domain):
    return True


while True:
    # Receive the domain from user
    try:
        domain = input("Enter the domain you want(q to stop): ")
        if domain == "q":
            break
        if check_domain(domain) is False:
            print("ERROR WITH THIS DOMAIN NAME, TRY AGAIN")
            continue
        msg = domain.encode('utf-8')
        print(f"SENDING DNS QUERY FOR {domain}")
        sock.sendto(msg, server_address)

        data, server = sock.recvfrom(BUFF)
        ip_add = data.decode('utf-8')
        print(f"THE IP FOR {domain} is {ip_add}")
    except socket.gaierror:
        print("COULD NOT FIND IP FOR THIS DOMAIN!")
    except socket.timeout:
        print("THAT IS NOT A VALID DOMAIN PLEASE TRY AGAIN")
    except Exception as e:
        print("ERROR: {e}")

sock.close()



