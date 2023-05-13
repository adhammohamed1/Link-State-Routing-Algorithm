COLOR_RED = 91
COLOR_GREEN = 92
COLOR_YELLOW = 93
COLOR_BLUE = 94
COLOR_MAGENTA = 95
COLOR_CYAN = 96
COLOR_WHITE = 97

def bold(text):
    return f"\033[1m{text}\033[0m"

def underline(text):
    return f"\033[4m{text}\033[0m"

def color(text, color):
    return f"\033[{color}m{text}\033[0m"

def set_color(color):
    return f"\033[{color}m"

def reset_format():
    return f"\033[0m"

def color_red(text):
    return color(text, COLOR_RED)

def color_green(text):
    return color(text, COLOR_GREEN)