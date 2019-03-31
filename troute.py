#!/usr/bin/env python3

import socket
import select
import struct
import sys
import requests
from random import randint
import time

UDP_START_DPORT = 33435
MAX_HOPS = 64
DATA_SIZE = 24

sys_msec = lambda: int(round(time.time() * 1000))

class flushfile(object):
    def __init__(self, stream):
       self.stream = stream
    def write(self, data):
       self.stream.write(data)
       self.stream.flush()
    def writelines(self, datas):
       self.stream.writelines(datas)
       self.stream.flush()
    def __getattr__(self, attr):
       return getattr(self.stream, attr)

def get_country_code(ip_addr_str):
    if ip_addr_str:
        try:
            url_str = "https://www.iplocate.io/api/lookup/" + ip_addr_str
        except:
            print(ip_addr_str)
            raise 'ip_addr_str'
        r = requests.get(url=url_str)
        if 'country_code' in r.json() and r.json()['country_code'] != None:
            return (r.json()['country_code'])
        else:
            return '**'
    else:
        return '**'

def get_host_info(host_addr):
    t1 = sys_msec()
    code = get_country_code(host_addr)
    try:
        host_name = socket.gethostbyaddr(host_addr)[0]
    except:
        host_name = host_addr
    diff = sys_msec() - t1
    return code, host_name, diff

def get_udp_port(packet):
    sport, dport = 0, 0
    icmp_header = packet[20:24]
    type, code, checksum = struct.unpack('bbH', icmp_header)
    #if type == 11 and code == 0 or type == 3 code == 3:
    inter_udp_header = packet[48:56]
    sp1, sp2, dp1, dp2, _, _ = struct.unpack('BBBBHH', inter_udp_header)
    sport = (sp1 << 8) + sp2
    dport = (dp1 << 8) + dp2
    return sport, dport

def traceroute(host_name):
    # icmp socket
    icmp = socket.getprotobyname('icmp')
    try:
        icmp_sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
    except:
        sys.stdout.write("%s\n" % "It is neededto run with root priviledge (use sudo) !")
        return
    icmp_sock.setblocking(0)

    # udp socket
    udp = socket.getprotobyname('udp')
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, udp)
    udp_sock.bind(('', 0))
    sport = udp_sock.getsockname()[1]

    # traceroute
    max_hops = MAX_HOPS
    coountry, host_addr, _ = get_host_info(host_name)
    host_addr = socket.gethostbyname(host_name)
    sys.stdout.write("\ntraceroute to %s (%s), %d hops max, %d bytes data" % 
        (host_name, host_addr, MAX_HOPS, DATA_SIZE))

    ttl = 1
    dport = UDP_START_DPORT
    curr_addr = None

    while curr_addr != host_addr and ttl < max_hops:
        # TTL
        udp_sock.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)

        # send udp
        tries = 3
        dport_dict = {}
        while tries > 0:
            dport_dict[dport] = [sys_msec(), '*', '']
            udp_sock.sendto(bytes(DATA_SIZE), (host_addr, dport))
            dport += 1
            tries = tries - 1

        # check response
        tries = 3
        got_resp = False
        last_addr = ''
        last_diff = 0
        sys.stdout.write("\n %2d  " % ttl)
        while tries > 0:
            ready = select.select([icmp_sock], [], [], 5)
            if ready[0]:
                packet, from_addr = icmp_sock.recvfrom(512)
                curr_addr = from_addr[0]
                sp, dp = get_udp_port(packet)
                if dp in dport_dict:
                    ms = sys_msec() - dport_dict[dp][0]
                    got_resp = True
                    if last_addr != curr_addr:
                        if last_addr != '':
                            sys.stdout.write("\n     ")
                        code, host_name, last_diff = get_host_info(curr_addr)
                        sys.stdout.write("%s - %s (%s) %s ms " % (code, host_name, curr_addr, ms))
                        last_addr = curr_addr
                    else:
                        ms = sys_msec() - dport_dict[dp][0] - last_diff
                        sys.stdout.write("%s ms " % (ms))
            else:
                sys.stdout.write("* ")
            tries = tries - 1

        ttl += 1

    udp_sock.close()
    icmp_sock.close()
    sys.stdout.write("\n\n")

if __name__ == "__main__":
    traceroute(sys.argv[1])

