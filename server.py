import socket
import threading
from datetime import datetime

HOST = '0.0.0.0'
PORT = 57890

clients = {}

def broadcast(message):
    for client in clients:
        try:
            client.sendall(message.encode())
        except:
            client.close()
            del clients[client]

def no_sender_broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.sendall(message.encode())
            except:
                client.close()
                del clients[client]

def handle_client(client_socket, addr):
    try:
        client_socket.send("Enter your nickname: ".encode())
        nickname = client_socket.recv(1024).decode().strip()
        clients[client_socket] = nickname

        no_sender_broadcast(f"{nickname} joined", client_socket)
        client_socket.send("Welcome!".encode())

        while True:
            message = client_socket.recv(1024).decode()
            if message.strip().lower() == "/quit":
                break
            if not message:
                break
            else:
                timestamp = datetime.now().strftime("%H:%M")
                broadcast(f"[{timestamp}] {nickname}: {message}", client_socket)

    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        if client_socket in clients:
            nickname = clients[client_socket]
            del clients[client_socket]
            no_sender_broadcast(f"{nickname} left the chat", client_socket)
        client_socket.close()
        
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    
    while True:
        client_socket, addr = server_socket.accept()

        thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        thread.start()

if __name__ == "__main__":
    start_server()