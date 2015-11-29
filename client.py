#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Programa cliente que abre un socket a un servidor
"""

import socket
import sys



print("\r\n")

# Cliente UDP simple.

# Dirección IP del servidor.
try:
    METODO = sys.argv[1]
    receptor = sys.argv[2] #batman@193.147.73.20:5555
    primer = receptor.split("@")
    LOGIN = primer[0]
    resto = primer[1].split(":")
    IP = resto[0]
    PUERTO = resto[1]
except:
    print("Usage: python3 client.py method receiver@IP:SIPport")
print(METODO + LOGIN + IP + PUERTO)
#login = separador.split(" ")[1]

#SERVER = 'localhost'
#PORT = 6001

# Contenido que vamos a enviar
#LINE = '¡Hola mundo!'
LINE = ("INVITE sip:" + LOGIN + "@" + IP + " SIP/2.0\r\n")

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
my_socket.connect((IP, int(PUERTO)))

print("Enviando: " + LINE)
my_socket.send(bytes(LINE, 'utf-8') + b'\r\n')

data = my_socket.recv(1024)
respuesta = data.decode('utf-8')
print('Recibido -- ' + respuesta)
serv_resp = respuesta.split(" ")
print(serv_resp)
if serv_resp[1] == "200":
    print("recv 200 ok")
    ack = "ACK sip:" + LOGIN + "@" + IP + " SIP/2.0\r\n"
    my_socket.send(bytes(ack, 'utf-8') + b'\r\n')
    print("enviado el ack")
#print("Terminando socket...")
# Cerramos todo
my_socket.close()
print("Fin.")
