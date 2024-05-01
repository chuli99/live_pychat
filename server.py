import socketserver
import messages

class ChatHandler(socketserver.BaseRequestHandler):
    rooms = {
        "programmers": [],
        "designers": [],
        "managers": []
    }

    def handle(self):
        
        print(f"New connection from {self.client_address}")
        self.request.sendall("Welcome to PyChat!\n".encode())
        #print(self.request)
        username = self.request.recv(512).decode()
        while True:    
            room = self.request.recv(512).decode().strip()
            print(room)
            room = room.lower()
            if room not in self.rooms:
                self.request.sendall("Invalid room. Closing connection.\n".encode())

            self.rooms[room].append(self.request)
            self.request.sendall(f"Welcome to {room} room!\n".encode())
            if messages.read_messages(room) == "missing file":
                pass
            else:
                for msgs in (messages.read_messages(room)):
                    self.request.sendall(msgs.encode())    
            while True:
                message = self.request.recv(512).decode().strip()
                if not message:
                    break
                if message == "exit":
                    print(self.client_address," remove.")
                    self.request.sendall("-exit-".encode())
                    self.rooms[room].remove(self.request)
                    print(len(self.rooms[room]))
                    break

                print(f"Received from {self.client_address}->{username}: {message} in:({room} room)")
                print(message)
                

                #Broadcast para enviar mensajes a todos los clientes en la misma sala:
                for client in self.rooms[room]:
                    try:
                        if client != self.request:
                            print(f"ENVIANDO:({self.client_address[0]}:{self.client_address[1]}->{username}): {message}")
                            sent_message = (f"({username})->{message}")
                            client.sendall(sent_message.encode())
                            #Guarda el mensaje en un txt
                            #messages.save_message(sent_message,room)
                    except:
                        client.close()
                        self.rooms[room].remove(client)
                        print(f"Connection from {client.getpeername()} closed due to error")

    def setup(self):
        pass

    def finish(self):
        for room, clients in self.rooms.items():
            if self.request in clients:
                clients.remove(self.request)
                print(f"Connection from {self.client_address} closed")

class ChatServer(socketserver.ThreadingTCPServer):
    def __init__(self, server_address, handler_class):
        super().__init__(server_address, handler_class)

if __name__ == "__main__":
    HOST, PORT = "localhost", 5554
    with ChatServer((HOST, PORT), ChatHandler) as server:
        print(f"Server started on {HOST}:{PORT}")
        server.serve_forever()
