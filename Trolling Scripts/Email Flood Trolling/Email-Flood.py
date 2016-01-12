#!/usr/bin/python
# -*- coding: utf-8 -*-

from email.mime.text import MIMEText
from email.MIMEMultipart import MIMEMultipart
import smtplib as s
import sys


#FUNÇÃO MAIN DO SISTEMA
def main():
    print banner()
    email_user = raw_input('INFORME SEU E-MAIL (GMAIL): ')
    email_pass = raw_input('INFORME SUA SENHA: ')

    validade,conn = test(email_user, email_pass)
    print '[!] CONEXÃO REALIZADA COM SUCESSO!'
    print conn
    if validade == True:
        send_emails(email_user,conn)
    else:
        print conn_error()
        sys.exit


#VALIDA O LOGIN E SENHA
def test(email_user, email_pass):
    try:
        conn = s.SMTP('smtp.gmail.com', 587)
        conn.starttls()
        conn.ehlo
        conn.login(email_user, email_pass)
        return True,conn

    except:
        print conn_error()


#RETORNA UM GUIA DE RESOLUÇÃO DE PROBLEMAS
def conn_error():
        print '[x] FALHA NA CONEXÃO'
        print '1º - VERIFIQUE SEU USUÁRIO E SENHA'
        print '2º - CERTIFIQUE-SE DE QUE HABILITOU OS APLICATIVOS MENOS SEGUROS'
        print 'URL: https://www.google.com/settings/security/lesssecureapps'
        return False



#ESSA FUNÇÃO É RESPONSÁVEL PELO ENVIO DOS EMAILS
def send_emails(email_user,conn):
    #Pega o e-mail da vítima
    FROM = email_user
    TO = raw_input('[!] INFORME O DESTINATÁRIO: ')

    #Escreve o e-mail
    SUBJECT = raw_input('[!] INFORME O ASSUNTO: ')
    text = raw_input('[!] ESCREVA UMA MENSAGEM: ')

    #Formata a mensagem nos padrões de envio SMTP
    message = MIMEMultipart()
    message['From'] = FROM
    message['To'] = TO
    message['Subject'] = SUBJECT
    message.attach(MIMEText(text, 'plain', 'utf-8'))
    email = message.as_string()

    #Envia o E-mail em looping
    while True:
        try:
            conn.sendmail(FROM, TO, email)
            print '[*] Floodando seu amigo... Pressione CTRL + C para cancelar'
        except:
            print '[x] Fail...'
            sys.exit()


#SÓ RETORNA UM BANNER COM ALGUNS AVISOS E EXPLICAÇÕES SOBRE A FERRAMENTA
def banner():
    banner = """
 ---|E-MAIL FLOOD SCRIPT|-----------------------------------------------------------------------------------
|                                                                                                           |
|   ESTE SCRIPT FOI PROJETO POR DIVERSÃO. ELE É PERFEITO PARA PEGADINHAS COM SEUS AMIGOS,                   |
|   MANDAR (MASSIVAS) MENSAGENS DE FELIZ ANIVERSÁRIO, BOAS FESTAS, DECLARAR SEU AMOR E TROLLAR              |
|   SEU GRUPO DE ESTUDAS DA FACULDADE.                                                                      |
|   EU NÃO SOU RESPONSÁVEL PELO USO INCORRETO DA FERRAMENTA. ALIÁS VOCÊ PODE MODIFICAR A VONTADE            |
|   ELA SÓ FUNCIONA COM O GMAIL E É NECESSÁRIA UMA PARAMETRIZAÇÃO DE SEGURANÇA PARA QUE ELA FUNCIONE BEM.   |
|   SUGIRO QUE PROSSIGA COM SEU E-MAIL FAKE :)                                                              |
|   ATIVE A OPÇÃO DE 'HABILITAR APLICATIVOS MENOS SEGUROS'                                                  |
|   URL: https://www.google.com/settings/security/lesssecureapps                                            |
|                                                                                                           |
|   ATENCIOSAMENTE: D0ctor                                                                                  |
 -----------------------------------------------------------------------------------------------------------

 """
    return banner

main()
