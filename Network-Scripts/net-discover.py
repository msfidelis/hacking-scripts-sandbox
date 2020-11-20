#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Matheus Fidelis aka D0ctor
# Github: https://github.com/msfidelis
# Web: http://nanoshots.com.br


#Usage: python net-discover.py 192.168.1.0/24

from netaddr import *
import os, sys
import subprocess
import multiprocessing as mp
import argparse


def discover(subnet):
    print ('[!] Starting network Scan to %s ' %subnet)
    hosts_up = mp.Queue()

    for host in IPNetwork(subnet):
        test = 'ping -c 1 -W2 %s >> /dev/null' % host
        #response,result = subprocess.run([test])

        response = os.system(test)
        if response == 0:
            print ('Host %s is UP' % host)
            hosts_up.put(host)
        else:
            print ('Host %s not avaliable' % host)
            pass
    print ('')
    print ('[*] LIVE HOSTS')
    while not hosts_up.empty():
        up = hosts_up.get()
        print ('[+] %s ' % up)

def main():
    parser = argparse.ArgumentParser(description = "Net Discovery", add_help = True, usage="Usage: python %(prog)s 192.168.1.0/24", prog="net-discover.py")
    parser.add_argument('namespace', help="namespace in format 192.168.1.0/24")
    args = parser.parse_args()
    subnet = args.namespace
    discover(subnet)

main()