#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import csv

#VARRE TODO O DIRETÓRIO E GERA UM CSV COM O NOME DAS PASTAS

def csv_writer(list):
    with open(csvpath, "a") as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        writer.writerow(list)


path = "/mnt/dados/nuvem/"
csvpath = "arquivos.csv"


for dirname, dirnames, filenames in os.walk(path):

    dir = dirname
    pasta = dir.replace(path, '')
    pasta = "'%s'" % pasta

    print pasta
    for file in  filenames:
        list = [pasta]
        file = "'%s'" % file
        list.append(file)

        csv_writer(list)
