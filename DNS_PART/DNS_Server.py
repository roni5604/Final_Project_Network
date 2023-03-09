import dns.resolver
import dns.query
import dns.message
import socketserver
import socket
import threading


class DNSServer(socketserver.ThreadingMixIn, socketserver.UDPServer):
    def __init__(self, server_address, RequestHandlerClass, resolver):
        self.resolver = resolver
        socketserver.UDPServer.__init__(self, server_address, RequestHandlerClass)


class DNSRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request[0]
        socket = self.request[1]
        query = dns.message.from_wire(data)

        # get the domain name from the query
        domain = query.question[0].name.to_text(omit_final_dot=True)
        print("Query for domain: " + domain)

        # use the resolver to lookup the IP address for the domain
        try:
            answer = self.server.resolver.query(domain)
            ip = answer[0].address
            print("IP address for domain: " + ip)
        except(dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.resolver.NoNameservers):
            print("Domain not found")
            return

        # create a response and add an answer section
        response = dns.message.make_response(query)
        response.set_rcode(dns.rcode.NOERROR)
        response.answer = [dns.rrset.from_text(domain, 60, dns.rdataclass.IN, dns.rdatatype.A, ip)]

        # send the response back to the client
        socket.sendto(response.to_wire(), self.client_address)


if __name__ == "__main__":
    resolver = dns.resolver.Resolver(cofigure=False)
    resolver.nameservers = ['8.8.8.8']  # use google's DNS server

    # create a DNS server and start listening for queries
    server = DNSServer(('127.0.0.1', 53), DNSRequestHandler, resolver)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()

    print("DNS server started on port 53")

    # run the server forever
    while True:
        server_thread.join(0.1)
