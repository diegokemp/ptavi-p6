#!/usr/bin/python3
# -*- coding: utf-8 -*-
import socketserver
import sys
import os


class SIPHandler(socketserver.DatagramRequestHandler):


    def handle(self):
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            line = self.rfile.read()
            IP_Client = str(self.client_address[0])
            try:
                lineutf = line.decode('utf-8')
            except UnicodeDecodeError:
                lineutf = ""
            if lineutf != "":
                #print("entra")
                method = lineutf.split(" sip:")
                metodos = ["INVITE","BYE","ACK"]
                if method[0] in metodos:
                    if method[0]=="INVITE":
                        self.wfile.write(b"SIP/2.0 100 Trying\r\n\r\n")
                        self.wfile.write(b"SIP/2.0 180 Ring\r\n\r\n")
                        self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
                        print(">TryingRingOK")
                    elif method[0]=="ACK":
                        os.system("chmod +x mp32rtp")
                        exe = "./mp32rtp -i " + IP_Client
                        exe = exe + " -p 23032 < " + audio_file
                        os.system(exe)
                        print(">audio_file enviado")
                    elif method[0]=="BYE":
                        self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
                        print(">OK")
                    else:
                        self.wfile.write(b"SIP/2.0 405 Method Not Allowed\r\n\r\n")
                        print(">405")
                    # Si no hay más líneas salimos del bucle infinito
            else:
                break

if __name__ == "__main__":
    try:
        IP = sys.argv[1]
        serv = socketserver.UDPServer(('', int(sys.argv[2])), SIPHandler)
        audio_file = sys.argv[3]
    except:
        print("Usage: python3 server.py IP port audio_file")
    print("Listening...")
    serv.serve_forever()
