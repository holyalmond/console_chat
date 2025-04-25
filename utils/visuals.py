import sys
from colorama import Fore

def clear_input_line():
    sys.stdout.write('\x1b[1A')
    sys.stdout.write('\x1b[2K')
    sys.stdout.flush()

def get_color(color):
    color = color.lower()
    color_map = {
        'black': Fore.BLACK,
        'red': Fore.RED,
        'green': Fore.GREEN,
        'yellow': Fore.YELLOW,
        'blue': Fore.BLUE,
        'magenta': Fore.MAGENTA,
        'cyan': Fore.CYAN,
        'white': Fore.WHITE,
        'reset': Fore.RESET
    }
    return color_map.get(color, Fore.RESET)
