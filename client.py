import socket
import threading
import menu, register, login, os, time, argparse
from subprocess import Popen, PIPE
from colorama import Fore, Style, Back
from getpass import getpass

def argparse_arguments():
    parser = argparse.ArgumentParser(description="Chat client")
    parser.add_argument("-ht","--host", type=str, help="Host to connect to", default="localhost")
    parser.add_argument("-p","--port", type=int, help="Port to connect to", default=5555)
    return parser.parse_args()



def receive_messages(sock):
    while True:
        message = sock.recv(512).decode()
        if not message:
            break
        if message == "-exit-":
            break
        print(message)

def send_messages(sock):
    while True:
        message = input("")
        sock.sendall(message.encode())
        if message == "exit":
            break

def connect_to_server(host, port):
    try:
        #Trying to connect with IPv6
        sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        sock.connect((host, port))
        return sock
    except Exception as e:
        print('IPv6 connection failed:', e)
        #If it fails, try to connect with IPv4
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((host, port))
            return sock
        except Exception as e:
            print('IPv4 connection failed:', e)
            return None

def main():
    rooms = ['programmers', 'designers', 'managers']
    args = argparse_arguments()
    HOST = args.host
    PORT = args.port
    sock = connect_to_server(HOST, PORT)
    
    if sock is None:
        print("Unable to connect to server.")
        return
    
    with sock:
        # Mensaje de bienvenida del servidor
        print(sock.recv(512).decode())

        while True:
            menu.show_login_register()
            choice = input("Choose an option:")
            if choice == "1":
                register.register()
                continue
            elif choice == "2":
                username = input("Enter username:")
                password = getpass("Enter password:")
                login_result = login.login(username, password)
                if login_result:
                    sock.sendall(username.encode())
                    break
                else:
                    continue
            elif choice == "3":
                exit()  
            else:
                print(Fore.RED + "Wrong option")
                print(Style.RESET_ALL)
        
        time.sleep(1)
        os.system('clear')
        while True:
            while True:
                menu.show_menu()
                option = input("Option:")
                os.system('clear')
                if option == "1":
                    menu.show_rooms()
                    room = input("Select room: <name_room>:").lower()
                
                    if room in rooms:
                        sock.sendall(room.encode())
                        os.system('clear')
                    
                        receive_msg_thread = threading.Thread(target=receive_messages, args=(sock,))
                        send_msg_thread = threading.Thread(target=send_messages, args=(sock,))
                
                        receive_msg_thread.start()
                        send_msg_thread.start()
                
                        # Esperar que ambos hilos terminen
                        receive_msg_thread.join() 
                        send_msg_thread.join()
                    
                        print(f"{Fore.RED}Leaving from {room} chat..")
                        print(Style.RESET_ALL)
                        time.sleep(3)
                        print(Back.GREEN + "See you soon!")
                        print(Style.RESET_ALL)
                        time.sleep(1)
                        break
                    else:
                        print("Please select a correct room")
                        continue
                elif option == "2":
                    exit()

main()