from commands.base import command, list_commands
from colorama import Fore, Style

@command(name="help", description="Show available commands")
def help(server, client, *args):
    message = Fore.CYAN + "Available commands:\n" + Style.RESET_ALL
    lines = [f"/{cmd.get('name')} - {cmd.get('description')}" for cmd in list_commands()]
    full_message = message + "\n".join(lines)
    client.conn.send(full_message.encode())
