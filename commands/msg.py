from commands.base import command
from utils.visuals import get_color

from datetime import datetime
from colorama import Fore, Style

@command(name="msg", description="Send private message with: /msg <nickname> <message>")
def online(server, client, *args):
    if not args or not args[0].strip():
        client.conn.send(f"{Fore.YELLOW}Error: use /msg <nickname> <message>{Style.RESET_ALL}".encode())
        return
    
    parts = args[0].split(" ", 1)
    if len(parts) < 2:
        client.conn.send(f"{Fore.YELLOW}Error: you must provide both a nickname and a message{Style.RESET_ALL}".encode())
        return

    nickname, message = parts[0].strip(), parts[1].strip()

    if not nickname or not message:
        client.conn.send(f"{Fore.YELLOW}Error: nickname or message cannot be empty{Style.RESET_ALL}".encode())
        return
    
    if nickname == client.nickname:
        client.conn.send(f"{Fore.YELLOW}Error: you cannot send a private message to yourself{Style.RESET_ALL}".encode())
        return
    
    receiver_sock = None
    for user_sock, user_info in server.clients.items():
        if user_info.get("nickname") == nickname:
            receiver_sock = user_sock
            break

    if receiver_sock is None:
        client.conn.send(f"{Fore.YELLOW}Error: user '{nickname}' not found on the server{Style.RESET_ALL}".encode())
        return
    
    timestamp = datetime.now().strftime("%H:%M")
    nickname_color = get_color(server.clients[client.conn]["color"])
    full_message = (f"{Fore.LIGHTBLACK_EX}[{timestamp}]{Style.RESET_ALL} "
                    f"{nickname_color}{client.nickname}{Style.RESET_ALL} (private): {message}")
    
    client.broadcast(full_message, receiver_sock=receiver_sock)
    client.conn.send(full_message.encode())