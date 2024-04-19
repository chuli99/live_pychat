import socketserver

class ChatHandler(socketserver.BaseRequestHandler):
    rooms = {
        "programmers": [],
        "designers": [],
        "managers": []
    }

    def handle(self):
        
        print(f"New connection from {self.client_address}")
        self.request.sendall("Welcome to PyChat!\n".encode())
        option = self.request.recv(512).decode().strip()
        room = option.lower()
        if room not in self.rooms:
            self.request.sendall("Invalid room. Closing connection.\n".encode())
            return
        self.rooms[room].append(self.request)
        self.request.sendall(f"Welcome to {room} room!\n".encode())

        while True:
            message = self.request.recv(512).decode().strip()
            if not message:
                break
            print(f"Received from {self.client_address}: {message} in:({room} room)")
            print(message)
            if message == "exit":
                print(self.client_address," remove.")
                client.close()
                self.rooms[room].remove(client)

            # Broadcast para enviar mensajes a todos los clientes en la misma sala:
            for client in self.rooms[room]:
                try:
                    if client != self.request:
                        client.sendall(f"({self.client_address[0]}:{self.client_address[1]}): {message}".encode())
                        
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
