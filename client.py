import socket
import sys
import argparse
import time, sys
    
def client(h,p):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error:
        print("Socket creation failed")
        sys.exit()
    
    #Recibe host por argumento
    host = h
    #Recibe port por argumento
    port = p
    print("Connecting..")
    time.sleep(2)
    s.connect((host,port))
    print("Handshake realizado")
    time.sleep(1)
    print("Esperando datos del server")
    while True:    
        user = input("Ingrese su usuario:")
        content = input("Ingrese un mensaje:")
        msg = (f"({user}): {content}")
        s.sendall(msg.encode('utf-8'))
        print("Enviando:",msg)
        print("Esperando datos del server")
        msg_server = s.recv(2048)  
        print(msg_server.decode('utf-8'))



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Comandos")
    parser.add_argument("-ht","--host",required=True,help="Dirección IP o nombre del servidor al que conectarse")
    parser.add_argument("-p","--port", type=int,required=True,help="Numero de puerto del servidor")
    args = parser.parse_args()
    print(args.host,args.port)

    client(args.host,args.port)
