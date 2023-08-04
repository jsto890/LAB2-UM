import numpy as np
from core import *

# Inputs
# f        : nonlinear function
# [a, b]     : initial interval of uncertainty
# max_iter : maximum number of iterations performed
# tol      : numerical tolerance used to check for root
# showlog  : True to output detailed steps
# Outputs
# xresult  : The result, i.e. the final x that minimises f(x)
# xlist    : list containing all x values where f(x) was evaluated
# flist    : list containing f(x) for all x in xmin
# k        : number of iterations (number of bisections)
# e        : ExitFlag (enumeration)


def brent(f,ab,max_iter,tol, showlog):
    a,b = ab # Unpack initial interval of uncertainty
    c = 0.5*(a + b)
    x1x2x3 = [a,b,c]
    fx1x2x3 = [f(x) for x in x1x2x3]
    flist=fx1x2x3[:]
    xlist=x1x2x3[:]
    
    if max(x1x2x3)-min(x1x2x3)<tol:
        return xlist[-1], xlist, flist, 0, ExitFlag.Converged

    for k in range(1,max_iter):
        denom=((x1x2x3[1]-x1x2x3[0])*(fx1x2x3[1]-fx1x2x3[2])-(x1x2x3[1]-x1x2x3[2])*(fx1x2x3[1]-fx1x2x3[0]))
        if abs(denom)<10e-18:
            if showlog:
                print(f'Brent iteration {k+1}')
                print(f'   denom = {denom} < 10e-18')
            return xlist[-1], xlist, flist, k, ExitFlag.DivideByZero
        x4=x1x2x3[1]-0.5*((x1x2x3[1]-x1x2x3[0])**2*(fx1x2x3[1]-fx1x2x3[2])-(x1x2x3[1]-x1x2x3[2])**2*(fx1x2x3[1]-fx1x2x3[0]))/((x1x2x3[1]-x1x2x3[0])*(fx1x2x3[1]-fx1x2x3[2])-(x1x2x3[1]-x1x2x3[2])*(fx1x2x3[1]-fx1x2x3[0]))
        f4 = f(x4)
        i=np.argmax(fx1x2x3)
        if showlog:
            print(f'Brent iteration {k+1}')
            for j in range(3):
                print(f'   x{j+1}={x1x2x3[j]:25.20f}, f{j+1}={fx1x2x3[j]:25.20f} {"  to become x4" if i==j else ""}')
            print(f'   x4={x4:25.20f}, f4={f4:25.20f}')
            print(f'   width={max(x1x2x3)-min(x1x2x3):25.20f}')
        x1x2x3[i]=x4
        fx1x2x3[i]=f4
        xlist.append(x1x2x3[i])
        flist.append(fx1x2x3[i])
        if max(x1x2x3)-min(x1x2x3)<tol:
            return xlist[-1], xlist, flist, k, ExitFlag.Converged

    if showlog:
        print(f'   Iteration limit reached')
    return xlist[-1], xlist, flist, k, ExitFlag.MaxIterations