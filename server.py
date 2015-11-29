#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import sys
import os


class EchoHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """

    def handle(self):
        # Escribe dirección y puerto del cliente (de tupla client_address)
        #self.wfile.write(b"Hemos recibido tu peticion")
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            line = self.rfile.read()
            IP_Client = str(self.client_address[0])
            print(IP_Client)
            lineutf = line.decode('utf-8')
            lineutf = lineutf.split(" sip:")
            #print(lineutf)
            metodos = ["INVITE","BYE","ACK"]
            if lineutf[0] in metodos:
                if lineutf[0]=="INVITE":
                    self.wfile.write(b"SIP/2.0 100 Trying\r\n\r\n")
                    self.wfile.write(b"SIP/2.0 180 Ring\r\n\r\n")
                    self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
                elif lineutf[0]=="ACK":
                    os.system("chmod 755 mp32rtp")
                    exe = "./mp32rtp -i " + IP_Client
                    exe = exe + " -p 23032 < " + audio_file
                    os.system(exe)
            # Si no hay más líneas salimos del bucle infinito

            if not line:
                break

if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    try:
        IP = sys.argv[1]
        serv = socketserver.UDPServer(('', int(sys.argv[2])), EchoHandler)
        audio_file = sys.argv[3]
    except:
        print("Usage: python3 server.py IP port audio_file")
    print("Listening...")
    serv.serve_forever()
