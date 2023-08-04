from enum import Enum

class ExitFlag(Enum):
    Converged = 0
    MaxIterations = 1
    NoRoot = 2
    DivideByZero = 3

global f_eval,g_eval
f_eval=0
g_eval=0

    
