from commands.base import command, list_commands
from colorama import Fore, Style

@command(name="help", help="Show available commands")
def help(sock, *args):
    print(Fore.CYAN + "\nAvailable commands:" + Style.RESET_ALL)
    for cmd in list_commands():
        print(f"/{cmd.get('name')} - {cmd.get('help')}")
    print()