import socket
import threading
from colorama import init, Fore, Style

from utils.visuals import clear_input_line

init(autoreset=True)

HOST = 'localhost'
PORT = 57890

def recieve_messages(sock):
    while True:
        try:
            message = sock.recv(1024).decode()
            if not message:
                break

            if message.endswith(":"):
                clear_input_line()
                print(f"{message} ", end="", flush=True)
            else:
                print(message)
        except:
            print(Fore.RED + "Disconnected from server." + Style.RESET_ALL)
            break

def send_messages(sock):
    while True:
        try:
            message = input()
            
            if message.strip().lower() == "/quit":
                print(Fore.RED + "Disconnecting from server..." + Style.RESET_ALL)
                sock.close()
                break

            clear_input_line()
            sock.sendall(message.encode())
        except:
            break

def start_client():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))

    print(Fore.MAGENTA + "Connected to chat server. Type /quit to exit" + Style.RESET_ALL)
    thread = threading.Thread(target=recieve_messages, args=(sock, ), daemon=True)
    thread.start()

    send_messages(sock)

if __name__ == "__main__":
    start_client()
            