import socket
import threading
from colorama import init, Fore, Style

from utils.visuals import clear_input_line
from utils.commands import commands, print_online_users

init(autoreset=True)

HOST = 'localhost'
PORT = 57890

online_users = []

def recieve_messages(sock):
    while True:
        try:
            message = sock.recv(1024).decode()
            if not message:
                break
            
            if message.startswith("@online_users "):
                users_string = message.replace("@online_users ", "")
                users = users_string.split(",") if users_string else []
                online_users.clear()
                online_users.extend(users)
                print_online_users(online_users)

            elif message.endswith(":"):
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
            if message.startswith("/"):
                parts = message[1:].split(maxsplit=1)
                cmd = parts[0].lower()
                args = parts[1] if len(parts) > 1 else ""
                handler = commands.get(cmd)
                if handler:
                    handler(sock, args)
                else:
                    print(Fore.YELLOW + f"Unknown command: /{cmd}" + Style.RESET_ALL)
            else:
                clear_input_line()
                sock.sendall(message.encode())
        except:
            break

def start_client():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))

    print(Fore.MAGENTA + "Connected to chat server." + Style.RESET_ALL)
    thread = threading.Thread(target=recieve_messages, args=(sock, ), daemon=True)
    thread.start()

    send_messages(sock)

if __name__ == "__main__":
    start_client()
            