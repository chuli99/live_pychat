import socket
import threading
from subprocess import Popen,PIPE


HOST, PORT = "localhost", 5554

def receive_messages(sock):
    while True:
        message = sock.recv(512).decode()
        if not message:
            break
        print(message)
        

def send_messages(sock):
    while True:
        message = input()
        sock.sendall(message.encode())
        if message.lower() == "exit":
            break

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((HOST, PORT))
    # Mensaje de bienvenida del server
    print(sock.recv(512).decode())

    #Inicializo hilo para recibir mensajes
    recieve_msg_thread = threading.Thread(target=receive_messages,args=(sock,))
    send_msg_thread = threading.Thread(target=send_messages,args=(sock,))

    send_msg_thread.start()
    recieve_msg_thread.start()
    #Esperar que ambos hilos terminen
    recieve_msg_thread.join() 
    send_msg_thread.join()

    