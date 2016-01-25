#!/usr/bin/python
# -*- coding: utf-8 -*-

import subprocess
import sys
import time

def geralog():
    #LOGS DO SISTEMA - Aqui selecionamos o nome do backup e o arquivo de logs que iremos criar.
    date = (time.strftime("%Y-%m-%d"))
    logfile     = '%s-backup-full.txt' % date
    pathlog     = '/var/log/backup/backup-full/%s' % logfile

    return pathlog

def gerabackup():
    date = (time.strftime("%Y-%m-%d"))
    backupfile  = '%s-backup-full.tar.gz' % date
    pathdestino = '/mnt/hdbackup/%s' % backupfile    # Destino onde será gravado o Backup
    pathorigem  = '/mnt/storage/'                    # pasta que será 'backupeada'
    backup      = 'tar cvf %s %s' % (pathdestino, pathorigem)

    return backup

def backupfull():
    pathlog = geralog()
    backup  = gerabackup()
    log         = ' >> %s' % pathlog

    #RODA O BACKUP
    subprocess.call(backup + log, shell=True)
    sys.exit()

backupfull()