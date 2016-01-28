#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
AUTORES: Matheus Fidelis
Script de Automação do Backup Full semanal e criação de Logs do Fileserver
para melhorar o script antigo escrito em Shellscript utilizando compactação via tar.gz

Talvez o ultimo script que eu escrevo como estagiário :)


  ==================================================================================
|| CONSIDERAÇÕES IMPORTANTES SOBRE O RSYNC
||  O Script pode ser modificado a vontade. Porém, ele foi criado de antemão
||  para os seguintes parâmetros que podem ser modificados na variável 'opts'
||  Dentro da função gerabackup(). Aqui vai uma explicação bem rápida sobre
||  cada um deles:
||
||  -v: Ativa a “verbosidade”. Simplesmente faz o rsync relatar todo o
||  processo na tela.
||
||  -q: Faz rsync trabalhar quietinho. Ele só printa alguns logs no final do
||  script. Ativem a opção e removam o -v caso queiram evitar logs muito grandes
||  no servidor :)
||
||   -r: Esse parâmetro é muito importante. Pois ele garante a recursividade do
||   Rsync. Ou seja, faz ele procurar arquivos e pastas dentro dos subdiretórios
||   Caso essa opção não seja ativada o Rsync vai sincronizar somente o primeiro
||   nível dos diretórios, ignorando as subpastas.
||
||  -n: rodada de testes. Serve para você testar o rsync sem correr o risco dele
||   modificar seus arquivos.
||
||   –delete: apaga arquivos do destino que não existam na origem. Este comando
||    garante que a origem e destino sejam exatamente iguais depois da sincronização.
||    Sem isso, o destino acumularia com arquivos que não existem mais na origem.
||    Desativá-lo pode ser útil para backups diários para manter um histórico.
||
||    -z: ativa a compressão, torna a transferência mais rápida.
||
||    -l, --links - cópia symlinks como symlinks
||
||    -L, --copy-links - transforma symlink em sua referência, arquivo ou diretório
||
||    -t, --times - preserva a data de modificação;
||
||    --exclude - exclui do backup alguns tipos de arquivos identificados pelo nome
||    pode ser utilizado para ignorar arquivos temporários e logs, como por exemplo
||      --exclude={'*.tmp,*.log'}
||
  ==================================================================================
'''

import subprocess
import time
import sys

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
    opts = 'rvtl'                                   # Opções que serão passadas com Rsync. Comentários no inicio do Script :)
    exclude = '*.log, *.tmp, .recycle'              # Define os diretórios e tipos de arquivos que não vão ter backup
    pathdestino = '/mnt/backupclone/'             # Destino onde será gravado espelhado o backup
    pathorigem  = '/mnt/storage/'                   # pasta que será 'backupeada'
    backup      = 'rsync -%s --exclude={%s} %s %s' % (opts, exclude, pathorigem, pathdestino) # Comando de execução

    #print backup
    #sys.exit()
    return backup


#CRIA OS BACKUPs
def backupclone():
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



backupclone()
