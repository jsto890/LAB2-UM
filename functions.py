import numpy as np

def f0(x):
    return x**4 - 8*x**3 + 24*x**2 - 32*x + 17
f0name = "f0"
f0title = "$f_{0}(x)=x^4-8x^3+24x^2-32x+17$"

def f1(x):
    return 2 - np.exp(-2*x**2 + 8*x - 8)
f1title = '$f_{1}(x)=2-exp(-2x^2+8x-8)$'

def f2(x):
    return x**2
f2title = '$f_{2}(x)=x^2$'

def f3(x):
    return x**4
f3title = '$f_{3}(x)=x^4$'

def f4(x):
    return x**6
f4title = '$f_{4}(x)=x^6$'

def f5(x):
    return x**8
f5title = '$f_{5}(x)=x^8$'

# Unused
def f6(x):
    return x**10
f6title = '$f_{6}(x)=x^{10}$'

task1functions = [f0,f1]
task1functiontitles = [f0title, f1title]

task3functions = [f2, f3, f4, f5]
task3functiontitles = [f2title, f3title, f4title, f5title]
