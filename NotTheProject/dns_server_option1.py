import dns.resolver
import dns.message
import dns.query

def dns_server():
    while True:
        data, addr = sock.recvfrom(512)
        req = dns.message.from_wire(data)
        name = str(req.question[0].name)
        qtype = req.question[0].rdtype

        try:
            answers = dns.resolver.query(name, qtype)
            resp = req.reply()
            for answer in answers:
                resp.add_answer(dns.rrset.from_rdata(qtype, name, answer))
            sock.sendto(resp.to_wire(), addr)
        except dns.exception.DNSException as e:
            print(e)
