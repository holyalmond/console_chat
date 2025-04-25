import socket
import threading
from datetime import datetime
from colorama import init, Fore, Style

from utils.visuals import get_color
from utils.visuals import color_map

init(autoreset=True)

HOST = '0.0.0.0'
PORT = 57890

clients = {}
color_map = color_map
used_colors = set()

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
        clients[client_socket] = {}

        client_socket.send("Enter your nickname: ".encode())
        nickname = client_socket.recv(1024).decode().strip()
        clients[client_socket]["nickname"] = nickname

        free_colors = [color for color in color_map if not color in used_colors]
        client_socket.send(f"Choose your color ({", ".join(free_colors)}): ".encode())
        color = client_socket.recv(1024).decode().strip()
        while color not in free_colors:
            client_socket.send(f"Invalid or taken color. Choose from: {', '.join(free_colors)}: ".encode())
            color = client_socket.recv(1024).decode().strip().lower()
        
        clients[client_socket]["color"] = color
        used_colors.add(color)

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
                msg_color = get_color(clients[client_socket]["color"])
                broadcast(
                    f"{Fore.LIGHTBLACK_EX}[{timestamp}]{Style.RESET_ALL} "
                    f"{msg_color}{nickname}{Style.RESET_ALL}: {message}"
                )

    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        if client_socket in clients:
            nickname = clients[client_socket]["nickname"]
            color = clients[client_socket]["color"]
            used_colors.discard(color)
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