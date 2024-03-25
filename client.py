import socket

HOST, PORT = "localhost", 5555

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((HOST, PORT))
    print(sock.recv(1024).decode())

    while True:
        message = input("Enter message: ")
        sock.sendall(message.encode())
        if message.lower() == "exit":
            break

        print("Esperando mensaje de otro cliente")
        recieve_message = sock.recv(1024).decode()
        print("Server saiys:",recieve_message)
