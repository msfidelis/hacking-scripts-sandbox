#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import csv
import subprocess

#CRIEI ESSE SCRIPT PRA VARRER TODOS OS DIRETÓRIOS A PARTIR DE UM ENDEREÇO ESPECÍFICO E MAPEAR TODOS OS ARQUIVOS,
#PASTAS, ME DIZER Q AUNTIDADE DE ARQUIVOS XML, PDF E JPG E GERAR UM CSV COM AS INFORMAÇÕES

# MAIS UM DIA DE PERIPÉCIAS DO MALANDRO NA FIRMA 


def csv_writer(list):
    with open(csvpath, "a") as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        writer.writerow(list)


path = "/home/matheus/teste/"
csvpath = "output.csv"

for dirname, dirnames, filenames in os.walk(path):

    dir = dirname
    pasta = dir.replace(path, '')
    pasta = "'%s'" % pasta
    list = [pasta]


    #Pega a quantidade geral
    commandtotal = 'ls -l %s | wc -l ; ' % dir
    qtd = subprocess.check_output(commandtotal, shell=True)
    qtd = qtd.rstrip()
    qtd = int(qtd) - 1
    qtd = "'%s'" % qtd

    list.append(qtd)


    #Pega a quantidade de PDF's
    commandpdf = 'ls -l %s/*.pdf | wc -l ;' % dir
    pdf = subprocess.check_output(commandpdf, shell=True)
    pdf = pdf.rstrip()
    pdf = "'%s'" % pdf

    list.append(pdf)


    #Pega a quantidade de arquivos JPG
    commandjpg = 'ls -l %s/*.jpg | wc -l ;' % dir
    jpg = subprocess.check_output(commandjpg, shell=True)
    jpg = jpg.rstrip()
    jpg = "'%s'" % jpg

    list.append(jpg)


    #Pega a quantidade de XML's
    commandxml = 'ls -l %s/*.xml | wc -l ;' % dir
    xml = subprocess.check_output(commandxml, shell=True)
    xml = xml.rstrip()
    xml = "'%s'" % xml

    list.append(xml)

    csv_writer(list)

