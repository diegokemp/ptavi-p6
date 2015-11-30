#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Programa cliente que abre un socket a un servidor
"""

import socket
import sys

try:
    METODO = sys.argv[1]
    receptor = sys.argv[2]
    primer = receptor.split("@")
    LOGIN = primer[0]
    resto = primer[1].split(":")
    IP = resto[0]
    PUERTO = resto[1]
except:
    print("Usage: python3 client.py method receiver@IP:SIPport")

LINE = (METODO + " sip:" + LOGIN + "@" + IP + " SIP/2.0\r\n")

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
my_socket.connect((IP, int(PUERTO)))

my_socket.send(bytes(LINE, 'utf-8') + b'\r\n')
i = 0
while i < 1:
    data = my_socket.recv(1024)
    respuesta = data.decode('utf-8')
    #print(respuesta)
    if respuesta != "":
    #print('Recibido -- ' + respuesta)
        serv_resp = respuesta.split(" ")
    #print(serv_resp)
        if serv_resp[1] == "200":
            print("cerrando cliente")#hemos enviado BYE, responde OK
            i = 2
        elif serv_resp[1] == "405":
            print(respuesta)
            i = 2
        elif serv_resp[1] == "100":#trying
            print(respuesta)
            findok = respuesta.split("\r\n\r\n")
            #print(findok)
            okmsg = findok[2].split(" ")
            if okmsg[2] == "OK":#3 mns concatenados Trying;Ring;OK
                ack = "ACK sip:" + LOGIN + "@" + IP + " SIP/2.0\r\n"
                my_socket.send(bytes(ack, 'utf-8') + b'\r\n')
                print(">Descargando...")
        elif serv_resp[1] == "180":#No deberia pasar por aqui
            print(respuesta)
    else:
        i = 2
#print("Terminando socket...")
# Cerramos todo
my_socket.close()
print(">Finalizado")
