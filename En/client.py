import sys
import socket
import threading
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QLineEdit, QPushButton, QTextEdit, 
                            QLabel, QMessageBox, QDialog, QFormLayout)
from PyQt5.QtCore import Qt, pyqtSignal, QObject

class ChatSignals(QObject):
    message_received = pyqtSignal(str)
    connection_error = pyqtSignal(str)

class ConnectionDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("연결 설정")
        self.resize(300, 150)
        
        layout = QFormLayout()
        
        self.host_input = QLineEdit("127.0.0.1")
        self.port_input = QLineEdit("5555")
        self.nickname_input = QLineEdit("사용자")
        
        layout.addRow("server IP:", self.host_input)
        layout.addRow("port:", self.port_input)
        layout.addRow("nickname:", self.nickname_input)
        
        self.connect_button = QPushButton("connect")
        self.connect_button.clicked.connect(self.accept)
        
        layout.addRow(self.connect_button)
        
        self.setLayout(layout)
    
    def get_connection_info(self):
        return (self.host_input.text(),
                int(self.port_input.text()),
                self.nickname_input.text())

class ChatClient(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.signals = ChatSignals()
        self.signals.message_received.connect(self.display_message)
        self.signals.connection_error.connect(self.show_error)
        
        self.client_socket = None
        self.connected = False
        
        self.init_ui()
        self.show_connection_dialog()
        
    def init_ui(self):
        self.setWindowTitle("chat client")
        self.resize(600, 400)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        
        # display the chat
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        layout.addWidget(self.chat_display)
        
        # type and send
        input_layout = QHBoxLayout()
        
        self.message_input = QLineEdit()
        self.message_input.returnPressed.connect(self.send_message)
        input_layout.addWidget(self.message_input)
        
        self.send_button = QPushButton("send")
        self.send_button.clicked.connect(self.send_message)
        input_layout.addWidget(self.send_button)
        
        layout.addLayout(input_layout)
        
        # connection status
        status_layout = QHBoxLayout()
        self.status_label = QLabel("connection: not connected")
        status_layout.addWidget(self.status_label)
        
        self.reconnect_button = QPushButton("re-connect")
        self.reconnect_button.clicked.connect(self.show_connection_dialog)
        status_layout.addWidget(self.reconnect_button)
        
        layout.addLayout(status_layout)
        
        central_widget.setLayout(layout)
    
    def show_connection_dialog(self):
        dialog = ConnectionDialog()
        if dialog.exec_():
            self.host, self.port, self.nickname = dialog.get_connection_info()
            self.connect_to_server()
    
    def connect_to_server(self):
        try:
            if self.client_socket:
                self.client_socket.close()
                
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.host, self.port))
            
            # set nickname
            message = self.client_socket.recv(1024).decode('utf-8')
            if message == "NICK":
                self.client_socket.send(self.nickname.encode('utf-8'))
            
            # start receive thread
            receive_thread = threading.Thread(target=self.receive_messages)
            receive_thread.daemon = True
            receive_thread.start()
            
            self.connected = True
            self.status_label.setText(f"연결 상태: {self.host}:{self.port}에 연결됨")
            
        except Exception as e:
            self.signals.connection_error.emit(f"서버 연결 실패: {str(e)}")
    
    def receive_messages(self):
        try:
            while True:
                message = self.client_socket.recv(1024).decode('utf-8')
                if message:
                    self.signals.message_received.emit(message)
                else:
                    # i no message was successfully sent, determine as connection lost
                    self.signals.connection_error.emit("connection with the server was lost")
                    self.connected = False
                    break
        except:
            self.signals.connection_error.emit("connectionwith the server was lost")
            self.connected = False
    
    def send_message(self):
        message = self.message_input.text().strip()
        if message and self.connected:
            try:
                self.client_socket.send(message.encode('utf-8'))
                self.message_input.clear()
            except:
                self.signals.connection_error.emit("메시지 전송 실패")
    
    def display_message(self, message):
        self.chat_display.append(message)
    
    def show_error(self, error_message):
        self.status_label.setText(f"connection status: {error_message}")
        QMessageBox.critical(self, "connection error", error_message)
    
    def closeEvent(self, event):
        if self.client_socket:
            self.client_socket.close()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    client = ChatClient()
    client.show()
    sys.exit(app.exec_())