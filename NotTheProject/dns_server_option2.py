import socket
import struct

# DNS header format (12 bytes)
# QID: query ID (2 bytes)
# QR: 0=query, 1=response (1 bit)
# OPCODE: operation code (4 bits)
# AA: authoritative answer (1 bit)
# TC: truncated message (1 bit)
# RD: recursion desired (1 bit)
# RA: recursion available (1 bit)
# Z: reserved (3 bits)
# RCODE: response code (4 bits)
# QDCOUNT: number of questions (2 bytes)
# ANCOUNT: number of answers (2 bytes)
# NSCOUNT: number of authority records (2 bytes)
# ARCOUNT: number of additional records (2 bytes)
DNS_HEADER_FORMAT = '>HHHHHH'

# DNS question format
# QNAME: question name (variable length)
# QTYPE: question type (2 bytes)
# QCLASS: question class (2 bytes)
DNS_QUESTION_FORMAT = '>{0}sHH'.format(len('www.example.com') + 1)

# DNS answer format
# NAME: name (variable length)
# TYPE: type (2 bytes)
# CLASS: class (2 bytes)
# TTL: time to live (4 bytes)
# RDLENGTH: length of RDATA field (2 bytes)
# RDATA: data (variable length)
DNS_ANSWER_FORMAT = '>{0}sHHIH{1}s'.format(len('www.example.com') + 1, socket.inet_aton('192.168.1.1').__len__())

# DNS response packet format
# Header (12 bytes)
# Question (variable length)
# Answer (variable length)
DNS_RESPONSE_FORMAT = DNS_HEADER_FORMAT + DNS_QUESTION_FORMAT + DNS_ANSWER_FORMAT

# DNS header fields
QR_QUERY = 0
QR_RESPONSE = 1
OPCODE_QUERY = 0
AA_NON_AUTHORITATIVE = 0
TC_NOT_TRUNCATED = 0
RD_NOT_DESIRED = 0
RA_NOT_AVAILABLE = 0
Z_RESERVED = 0
RCODE_NO_ERROR = 0

# DNS question fields
QTYPE_A = 1
QCLASS_IN = 1


def handle_dns_query(data, addr):
    # Unpack DNS query
    qid, flags, qdcount, ancount, nscount, arcount = struct.unpack(DNS_HEADER_FORMAT, data[:12])
    qname, qtype, qclass = struct.unpack_from(DNS_QUESTION_FORMAT, data, 12)
    qname = qname.rstrip(b'\0').decode('utf-8')

    # Prepare DNS response
    if flags & QR_QUERY == QR_QUERY and qdcount == 1:
        resp_flags = QR_RESPONSE << 15 | OPCODE_QUERY << 11 | AA_NON_AUTHORITATIVE << 10 | TC_NOT_TRUNCATED << 9 | \
                     RD_NOT_DESIRED << 8 | RA_NOT_AVAILABLE << 7 | Z_RESERVED << 4 | RCODE_NO_ERROR
        resp_qdcount = qdcount
        resp_ancount = 1
        resp_nscount = 0
        resp_arcount = 0
        resp_question = struct.pack(DNS_QUESTION_FORMAT, qname.encode('utf-8'), qtype, qclass)
        resp_answer = struct.pack(DNS_ANSWER_FORMAT, qname.encode('utf-8'), QTYPE_A, QCLASS_IN, 60, 4, socket.inet_aton('192.168.1.1'))

        # Pack DNS response
        # resp = struct.pack(DNS_RESPONSE_FORMAT, q
