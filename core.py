from enum import Enum


class ExitFlag(Enum):
    Converged = 0
    MaxIterations = 1
    NoRoot = 2
    DivideByZero = 3


global f_eval,g_eval
f_eval=0
g_eval=0


# Coloriser of unique values in output
PURPLE = '\033[95m'
CYAN = '\033[96m'
DARKCYAN = '\033[36m'
BLUE = '\033[94m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'
endcolor = '\033[0m'

colors = [CYAN, BLUE, GREEN, YELLOW, RED,]
# '\033[95m', # header
# '\033[94m', # blue
# '\033[96m' # cyan
# '\033[92m', #green
# '\033[93m', # warning
# '\033[91m', # fail
# '\033[0m', #endc
# '\033[1m', #bold
# '\033[4m', #underline
lastcolor = 0
coloursused = {}


def color(x):
    global lastcolor
    global coloursused
    c = coloursused.get(x)
    if not c:
        lastcolor = (lastcolor+1) % len(colors)
        c = lastcolor
        coloursused[x] = c
    return colors[c]
