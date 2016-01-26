#!/usr/bin/python2.s7
# -*- coding: utf-8 -*-
# Author: Matheus Fidelis aka D0ctor
# Github: https://github.com/msfidelis
# Web: http://nanoshots.com.br


#Usage: python net-discover.py 192.168.1.0/24

from netaddr import *
import os, Queue, sys
import subprocess


def discover(subnet):
    print ' ================================================='
    print '       [!] Starting network Scan to %s            '  % subnet
    print ' ================================================='
    hosts_up = Queue.Queue()
    for host in IPNetwork(subnet):
        test = 'ping -c 1 -w2 %s >> /dev/null' % host
        #response,result = subprocess.run([test])

        response = os.system(test)
        if response == 0:
            print ' |   [!] Host %s is UP' % host
            hosts_up.put(host)
        else:
            print ' |   [x] Host %s not avaliable' % host
            pass
    print ''
    print ' ================================================='
    print '                [*] LIVE HOSTS                   '
    print ' ================================================='
    while not hosts_up.empty():
        up = hosts_up.get()
        print '[+] %s ' % up


subnet = sys.argv[1]

discover(subnet)
