import socket
import threading
from datetime import datetime
from colorama import init, Fore, Style

init(autoreset=True)

HOST = '0.0.0.0'
PORT = 57890

clients = {}

def broadcast(message, sender_socket=None):
    for client in clients.copy():
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

        broadcast(Fore.GREEN + f"{nickname} joined" + Style.RESET_ALL, client_socket)
        client_socket.send((Fore.LIGHTGREEN_EX + "Welcome!" + Style.RESET_ALL).encode())

        while True:
            message = client_socket.recv(1024).decode()
            if message.strip().lower() == "/quit":
                break
            if not message:
                break
            else:
                timestamp = datetime.now().strftime("%H:%M")
                broadcast(
                    f"{Fore.LIGHTBLACK_EX}[{timestamp}]{Style.RESET_ALL} "
                    f"{Fore.BLUE}{nickname}{Style.RESET_ALL}: {message}"
                )

    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        if client_socket in clients:
            nickname = clients[client_socket]
            del clients[client_socket]
            broadcast(Fore.GREEN + f"{nickname} left the chat" + Style.RESET_ALL, client_socket)
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