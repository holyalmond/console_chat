import sys

def clear_input_line():
    sys.stdout.write('\x1b[1A')
    sys.stdout.write('\x1b[2K')
    sys.stdout.flush()

def set_color():
    pass