#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import sys


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
            lineutf = line.decode('utf-8')
            lineutf = lineutf.split(" sip:")
            print(lineutf)
            metodos = ["INVITE","BYE","ACK"]
            if lineutf[0] in metodos:
                if lineutf[0]=="INVITE":
                    #self.wfile.write(b"SIP/2.0 100 Trying\r\n")
                    #self.wfile.write(b"SIP/2.0 180 Ring\r\n")
                    self.wfile.write(b"SIP/2.0 200 OK\r\n")
                elif lineutf[0]=="ACK":
                    print("enviando cancion")
                    self.wfile.write(b"CANCION INCOMING")
            else:
                print("mal asunto")
                #self.wfile.write(b"SIP/2.0 405 Method Not Allowed\r\n")

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
