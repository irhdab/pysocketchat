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
        print(f"서버가 {self.host}:{self.port}에서 실행 중입니다.")
        print("클라이언트 연결을 기다리는 중...")
        
        while True:
            client_socket, address = self.server_socket.accept()
            print(f"새로운 연결: {address}")
            
            # 클라이언트로부터 닉네임 받기
            client_socket.send("NICK".encode('utf-8'))
            nickname = client_socket.recv(1024).decode('utf-8')
            
            self.nicknames.append(nickname)
            self.clients.append(client_socket)
            
            # 연결 알림
            print(f"{nickname}({address})이(가) 연결되었습니다.")
            self.broadcast(f"{nickname}님이 채팅방에 참여했습니다!".encode('utf-8'))
            client_socket.send("서버에 연결되었습니다!".encode('utf-8'))
            
            # 각 클라이언트를 위한 스레드 시작
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
                    # 메시지가 없으면 연결이 끊어진 것으로 간주
                    self.remove_client(client_socket, nickname)
                    break
        except:
            self.remove_client(client_socket, nickname)
    
    def broadcast(self, message):
        for client in self.clients:
            try:
                client.send(message)
            except:
                # 메시지 전송 중 오류가 발생하면 클라이언트 제거
                self.remove_client(client, self.nicknames[self.clients.index(client)])
    
    def remove_client(self, client_socket, nickname):
        if client_socket in self.clients:
            index = self.clients.index(client_socket)
            self.clients.remove(client_socket)
            client_socket.close()
            nickname = self.nicknames.pop(index)
            self.broadcast(f"{nickname}님이 채팅방을 나갔습니다.".encode('utf-8'))
            print(f"{nickname}이(가) 연결을 종료했습니다.")

if __name__ == "__main__":
    # 기본값으로 서버 실행
    host = input("서버 IP 주소 (기본: 127.0.0.1): ") or '127.0.0.1'
    port = input("포트 번호 (기본: 5555): ") or 5555
    server = ChatServer(host, int(port))
    server.start()
