from core import *
import numpy as np

# Inputs
# f        : nonlinear function
# [a, b]   : initial interval of uncertainty
# max_iter : maximum number of iterations performed
# tol      : requred interval of uncertainty
# showlog  : True to output detailed steps
# Outputs
# [a,b]    : the result, i.e. the final interval of uncertainty
# xlist    : list containing all x values where f(x) was evaluated
# flist    : list containing f(x) for all x in xmin
# k        : number of iterations (number of bisections)
# e        : ExitFlag (enumeration)


def golden(f, ab, max_iter, tol, showlog):
    a,b = ab # Unpack initial interval of uncertainty
    tau = 0.5*(np.sqrt(5) - 1)

    # We start by setting x'=alpha; our first iteration below will end up setting x''=beta
    alpha = a + (1 - tau)*(b - a)
    xd = alpha
    fd = f(xd)

    xlist=[xd]
    flist=[fd]

    for k in range(max_iter):
        if xd <= (a + b) / 2:
            xdd = a + (1 - tau) * (b - a)
        else:
            xdd = a + tau * (b - a)

        fdd = f(xdd)
        xlist.append(xdd)
        flist.append(fdd)

        if fdd <= fd:
            if xd <= (a + b) / 2:
                b = xd
            else:
                a = xd
        else:
            if xd <= (a + b) / 2:
                a = xdd
            else:
                b = xdd

        xd = xdd
        fd = fdd

        if b - a <= tol:
            return [a, b], xlist, flist, k, ExitFlag.Converged

    return [a, b], xlist, flist, max_iter, ExitFlag.MaxIterations


def logiteration(k,a,alpha,beta,b, falpha, fbeta, showlog):
    if showlog:
        print(f'{k:2}: {a:20.15f}{"*" if falpha <= fbeta else " "} {alpha:20.15f}* {beta:20.15}* {d:20.15f}{"*" if falpha > fbeta else " "}')
        print(f'                          {falpha:20.15f}  {fbeta:20.15f}  ')
