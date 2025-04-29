import socket
from commands.base import command
from colorama import Fore, Style

@command(name="quit", description="Leave the chat")
def quit(server, client, *args):
    client.conn.send((Fore.RED + "Disconnecting from server..." + Style.RESET_ALL).encode())
    client.running = False
    client.conn.shutdown(socket.SHUT_RDWR)
    client.conn.close()
