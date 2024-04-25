import socket
import threading
import menu, register, login
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

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    rooms = ['programmers','designers','managers']
    sock.connect((HOST, PORT))
    # Mensaje de bienvenida del server
    print(sock.recv(512).decode())
    
    while True:
        menu.show_login_register()
        choice = input("Choose an option:")
        if choice == "1":
            register.register()
            break
        elif choice == "2":
            username = input("Enter username:")
            password = input("Enter password:")
            login_result = login.login(username,password)
            if login_result == True:
                break
            else:
                continue
        elif choice == "3":
            break  
        
        else:
            print("Wrong option")
    
    while True:
        sock.sendall(username.encode())
        menu.show_menu()
        option = input("Option:")
        if option == "1":
            print("Chat P2P is not available")
        elif option == "2":
            menu.show_rooms()
            room = input("Select rooms: <name_room>:")
            if room.lower() in rooms:
                #Inicializo hilo para recibir mensajes
                sock.sendall(room.encode())
                recieve_msg_thread = threading.Thread(target=receive_messages,args=(sock,))
                send_msg_thread = threading.Thread(target=send_messages,args=(sock,))

                send_msg_thread.start()
                recieve_msg_thread.start()
                #Esperar que ambos hilos terminen
                recieve_msg_thread.join() 
                send_msg_thread.join()
            else:
                print("Please select a correct room")
                continue
        elif option == 3:
            break
    