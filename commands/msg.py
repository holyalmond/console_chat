from commands.base import command
from utils.visuals import get_color

from datetime import datetime
from colorama import Fore, Style

@command(name="msg", description="Send private message with: /msg nickname message")
def online(server, client, *args):
    if args:
        parts = args[0].split(" ", 1)
        nickname, message = parts
    for user_sock, user_info in server.clients.items():
        if user_info.get("nickname") == nickname:
            receiver_sock = user_sock
    timestamp = datetime.now().strftime("%H:%M")
    nickname_color = get_color(server.clients[client.conn]["color"])
    full_message = (f"{Fore.LIGHTBLACK_EX}[{timestamp}]{Style.RESET_ALL} "
                    f"{nickname_color}{client.nickname}{Style.RESET_ALL}(private): {message}")
    client.broadcast(full_message, receiver_sock=receiver_sock)
    client.conn.send(full_message.encode())