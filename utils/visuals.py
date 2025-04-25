import sys
from colorama import Fore

def clear_input_line():
    sys.stdout.write('\x1b[1A')
    sys.stdout.write('\x1b[2K')
    sys.stdout.flush()

color_map = {
        'black': Fore.BLACK,
        'red': Fore.RED,
        'green': Fore.GREEN,
        'yellow': Fore.YELLOW,
        'blue': Fore.BLUE,
        'magenta': Fore.MAGENTA,
        'cyan': Fore.CYAN,
        'white': Fore.WHITE
    }

def get_color(color):
    color = color.lower()
    return color_map.get(color, Fore.RESET)

def set_color(client_socket, used_colors):
    free_colors = [color for color in color_map if not color in used_colors]
    client_socket.send(f"Choose your color ({", ".join(free_colors)}):".encode())
    color = client_socket.recv(1024).decode().strip().lower()
    while color not in free_colors:
        client_socket.send(f"Invalid or taken color. Choose from: {', '.join(free_colors)}:".encode())
        color = client_socket.recv(1024).decode().strip().lower()
    used_colors.add(color)

    return color