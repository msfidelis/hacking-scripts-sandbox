#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
AUTORES: Matheus Fidelis
Script de Automação do Backup Full semanal e criação de Logs do Fileserver
para melhorar o script antigo escrito em Shellscript utilizando compactação via tar.gz

Talvez o ultimo script que eu escrevo como estagiário :)
'''

import subprocess
import time

#Essa função gera um banner com a hora inicial do Backup
def inicio(horaInicio):

    inicio = '''
  ===========================================================================
||  ____          _____ _  ___    _ _____    _____   _____                   ||
|| |  _ \   /\   / ____| |/ / |  | |  __ \  |  __ \ / ____|                  ||
|| | |_) | /  \ | |    | ' /| |  | | |__) | | |__) | (___  _   _ _ __   ___  ||
|| |  _ < / /\ \| |    |  < | |  | |  ___/  |  _  / \___ \| | | | '_ \ / __| ||
|| | |_) / ____ \ |____| . \| |__| | |      | | \ \ ____) | |_| | | | | (__  ||
|| |____/_/    \_\_____|_|\_ \____/|_|      |_|  \_\_____/ \__, |_| |_|\___| ||
||                                                          __/ |            ||
||                                                         |___/             ||
||                    BACKUP DIFERENCIAL DO FILESERVER                       ||
  ===========================================================================

  ===========================================================================
                BACKUP DIFERENCIAL DO FILESERVER INICIADO ÀS %s
  ===========================================================================
''' % horaInicio
    return inicio

#Termino e calculos
def termino(diaInicio, horaInicio, backup, pathlog):
    hoje = (time.strftime("%d-%m-%Y"))
    horaFinal   = time.strftime('%H:%M:%S')
    backup = backup.replace('tar cvf', '')
    final = '''
  ===========================================================================
                            BACKUP FULL FINALIZADO

                HORA INICIAL:    %s  -  %s
                HORA FINAL  :    %s  -  %s
                LOG FILE    :    %s
                BAK FILE    :    %s
  ===========================================================================

    ''' % (diaInicio, horaInicio, hoje, horaFinal, pathlog, backup)
    return final


#CONSTROI OS LOGS DO SISTEMA - Aqui selecionamos o nome do backup e o arquivo de logs que iremos criar.
def geralog():
    date = (time.strftime("%Y-%m-%d"))              #
    logfile     = '%s-backup-rsync.txt' % date       # Cria o arquivo de Log
    pathlog     = '/var/log/backup/backup-rsync/%s' % logfile    # Arquivo de log

    return pathlog


#CONSTROI O ARQUIVO E PATH DE BACKUP E RETORNA
def gerabackup():
    date = (time.strftime("%Y-%m-%d"))
    backupfile  = '%s-backup-full.tar.gz' % date    # Cria o nome do arquivo de Backup
    pathdestino = '/mnt/hdbackup/%s' % backupfile   # Destino onde será gravado o Backup
    pathorigem  = '/mnt/storage/'                   # pasta que será 'backupeada'
    backup      = 'tar cvf %s %s' % (pathdestino, pathorigem) # Comando de execução

    return backup


#CRIA OS BACKUPs
def backupfull():
    horaInicio  = time.strftime('%H:%M:%S')
    pathlog     = geralog()
    backup      = gerabackup()
    log         = ' >> %s' % pathlog
    start       = inicio(horaInicio)

    #Printa o Banner
    l = open(pathlog, 'w')
    l.write(start)
    l.close()

    #RODA O BACKUP
    subprocess.call(backup + log, shell=True)

    #Printa o final e relatório
    diaInicio   = (time.strftime("%d-%m-%Y"))
    final       = termino(diaInicio, horaInicio, backup, pathlog)
    r           = open(pathlog, 'w')
    r.write(final)
    r.close()



backupfull()
