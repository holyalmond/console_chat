from colorama import Fore, Style

commands = {}

def client_command(name):
    def decorator(func):
        commands[name] = func
        return func
    return decorator

@client_command("help")
def help_command(sock, *args):
    print(Fore.CYAN + "\nAvailable commands:" + Style.RESET_ALL)
    for cmd in commands.keys():
        print(f"/{cmd}")
    print("\n")

@client_command("quit")
def quit_command(sock, *args):
    print(Fore.RED + "Disconnecting from server..." + Style.RESET_ALL)
    sock.close()
    exit(0)
