import socket
import threading

class ChatServer:
    def __init__(self, host='127.0.0.1', port=5555):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.clients = []
        self.nicknames = []

    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"server is running at {self.host}:{self.port}.")
        print("Wating for client connection . . .")
        
        while True:
            client_socket, address = self.server_socket.accept()
            print(f"new connection: {address}")
            
            # get nickname from the client
            client_socket.send("NICK".encode('utf-8'))
            nickname = client_socket.recv(1024).decode('utf-8')
            
            self.nicknames.append(nickname)
            self.clients.append(client_socket)
            
            # connection notification 
            print(f"{nickname}({address}) connected.")
            self.broadcast(f"{nickname} joined the chat room".encode('utf-8'))
            client_socket.send("connected to the server".encode('utf-8'))
            
            # thread for the client
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket, nickname))
            client_thread.daemon = True
            client_thread.start()
    
    def handle_client(self, client_socket, nickname):
        try:
            while True:
                message = client_socket.recv(1024)
                if message:
                    self.broadcast(f"{nickname}: {message.decode('utf-8')}".encode('utf-8'))
                else:
                    # if no message was sent, remove client 
                    self.remove_client(client_socket, nickname)
                    break
        except:
            self.remove_client(client_socket, nickname)
    
    def broadcast(self, message):
        for client in self.clients:
            try:
                client.send(message)
            except:
                # remove client if the connection was lost
                self.remove_client(client, self.nicknames[self.clients.index(client)])
    
    def remove_client(self, client_socket, nickname):
        if client_socket in self.clients:
            index = self.clients.index(client_socket)
            self.clients.remove(client_socket)
            client_socket.close()
            nickname = self.nicknames.pop(index)
            self.broadcast(f"{nickname} leaved the chat room.".encode('utf-8'))
            print(f"{nickname} has disconnected")

if __name__ == "__main__":
    # run server as default
    # default address for ip is 127.0.0.1 localhost, and the port number is 5555
    host = input("custom server ip(yours)") or '127.0.0.1'
    port = input("port number (any)") or 5555
    server = ChatServer(host, int(port))
    server.start()