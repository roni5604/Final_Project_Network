import dns.message
import dns.rcode
import dns.server
import dns.query


class DNSHandler:
    def handle_request(self, request, address):
        # Process the DNS request
        print(f"Received DNS request for {request.question[0].name}")
        response = dns.message.Message(request.id)
        response.question = request.question
        response.set_opcode(request.opcode())
        response.set_rcode(dns.rcode.NOERROR)

        # Add the DNS resource record(s) to the response
        rrset = dns.rrset.RRset(request.question[0].name, dns.rdataclass.IN, dns.rdatatype.A)
        rrset.add(dns.rrset.Rdata(dns.rdataclass.IN, dns.rdatatype.A, '192.0.2.1'))
        response.answer.append(rrset)

        # Send the DNS response
        dns.query.udp(response.to_wire(), address[0])


if __name__ == '__main__':
    handler = DNSHandler()
    server = dns.server.ThreadingUDPServer(('127.0.0.1', 53), handler)
    server.serve_forever()
