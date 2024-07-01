import socketserver, socket, threading
import messages

class ChatHandler(socketserver.BaseRequestHandler):
    rooms = {
        "programmers": [],
        "designers": [],
        "managers": []
    }
    rooms_lock = threading.Lock()  

    def handle(self):
        
        print(f"New connection from {self.client_address}")
        self.request.sendall("Welcome to PyChat!\n".encode())
        username = self.request.recv(512).decode()
        while True:    
            room = self.request.recv(512).decode().strip()
            print(room)
            room = room.lower()
            if room not in self.rooms:
                self.request.sendall("Invalid room. Closing connection.\n".encode())

            with self.rooms_lock:  
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
                    print(self.client_address, " remove.")
                    self.request.sendall("-exit-".encode())
                    with self.rooms_lock:  
                        self.rooms[room].remove(self.request)  
                    print(len(self.rooms[room]))
                    break

                print(f"Received from {self.client_address}->{username}: {message} in:({room} room)")
                
                #Save message in txt
                sent_message = (f"({username})->{message}")
                print("Saving message")
                messages.save_message(sent_message, room)

                #Broadcast para enviar mensajes a todos los clientes en la misma sala:
                with self.rooms_lock:  
                    clients = self.rooms[room][:]  
                for client in clients:
                    try:
                        if client != self.request:
                            print(f"SENDING:({self.client_address[0]}:{self.client_address[1]}->{username}): {message}")
                            client.sendall(sent_message.encode())
                    except:
                        client.close()
                        with self.rooms_lock:  
                            self.rooms[room].remove(client)
                        print(f"Connection from {client.getpeername()} closed due to error")

    def setup(self):
        pass

    def finish(self):
        with self.rooms_lock:  
            for room, clients in self.rooms.items():
                if self.request in clients:
                    clients.remove(self.request)
                    print(f"Connection from {self.client_address} closed")

class ChatServerIPV4(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass
        

class ChatServerIPV6(socketserver.ThreadingMixIn, socketserver.TCPServer):
    address_family = socket.AF_INET6
    pass  


def connections(address):
    if address[0] == socket.AF_INET:
        with ChatServerIPV4((HOST, PORT), ChatHandler) as server:
            print(f"Server started on {HOST}:{PORT}")
            server.serve_forever()
    
    elif address[0] == socket.AF_INET6:
        with ChatServerIPV6((HOST_6, PORT_6), ChatHandler) as server:
            print(f"Server started on {HOST_6}:{PORT_6}")
            server.serve_forever()
            

if __name__ == "__main__":
    HOST, PORT = "localhost", 5555
    HOST_6, PORT_6 = "::1", 5556
    socketserver.TCPServer.allow_reuse_address = True
    addresses = socket.getaddrinfo(None, PORT_6, socket.AF_UNSPEC, socket.SOCK_STREAM,socket.IPPROTO_TCP)
    threads = []
    for a in addresses:
        threads.append(threading.Thread(target=connections, args=(a,)))
    for t in threads:
        t.start()
