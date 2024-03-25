import socketserver

class ChatHandler(socketserver.BaseRequestHandler):
    def handle(self):
        print(f"New connection from {self.client_address}")
        self.request.sendall("Welcome to the chat server!\n".encode())

        while True:
            message = self.request.recv(1024).decode().strip()
            if not message:
                break
            print(f"Received from {self.client_address}: {message}")

            # Broadcast the message to all clients
            for client in self.server.clients:
                print(len(self.server.clients))
                try:
                    if client != self.request:
                        client.sendall(f"{self.client_address[0]}:{self.client_address[1]} says: {message}\n".encode())
                except:
                    client.close()
                    self.server.clients.remove(client)
                    print(f"Connection from {client.getpeername()} closed due to error")

    def setup(self):
        self.server.clients.append(self.request)

    def finish(self):
        self.server.clients.remove(self.request)
        print(f"Connection from {self.client_address} closed")

class ChatServer(socketserver.ThreadingTCPServer):
    def __init__(self, server_address, handler_class):
        super().__init__(server_address, handler_class)
        self.clients = []

if __name__ == "__main__":
    HOST, PORT = "localhost", 5555
    with ChatServer((HOST, PORT), ChatHandler) as server:
        print(f"Server started on {HOST}:{PORT}")
        server.serve_forever()
