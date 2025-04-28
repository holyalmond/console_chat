from colorama import Fore, Style
from utils.visuals import get_color

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
    print()

@client_command("quit")
def quit_command(sock, *args):
    print(Fore.RED + "Disconnecting from server..." + Style.RESET_ALL)
    sock.close()
    exit(0)

def print_online_users(users):
    if users:
        print(Fore.LIGHTGREEN_EX + "\nOnline users:" + Style.RESET_ALL)
        for user_info in users:
            if ":" in user_info:
                nickname, color = user_info.split(":")
                print(f"{get_color(color)}{nickname}{Style.RESET_ALL}")
            else:
                print(user_info)
        print()
    else:
        print("No users online.")

@client_command("online")
def online_command(sock, *args):
    try:
        sock.send("@request_online_users".encode())
    except Exception as e:
        print(Fore.RED + f"Failed to request online users: {e}" + Style.RESET_ALL)

