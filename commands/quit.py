from commands.base import command
from colorama import Fore, Style

@command(name="quit", help="Leave the chat")
def quit(sock, *args):
    print(Fore.RED + "Disconnecting from server..." + Style.RESET_ALL)
    sock.close()
    exit(0)