import numpy as np
from core import ExitFlag, color, endcolor

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
zerotol = 10e-18


def fullbrent(f,ab,max_iter,tol, showlog):
    a,b = ab # Unpack initial interval of uncertainty

    # Create our constants and one first initial point xd
    tau = 0.5*(np.sqrt(5) - 1)
    rho = 0.5*(3-np.sqrt(5))
    xd = a + (1 - tau)*(b - a)
    fd = f(xd)

    # Initialise our record of function evaluations and the x & f values used for the quadratic
    xlist=[xd]
    flist=[fd]
    x1x2x3 = [xd]
    fx1x2x3 = [fd]

    # Test for convergence
    k=0
    if b-a<tol:
        logfinal(f, k, a, b, tol, showlog)
        return [a,b], xlist, flist, k, ExitFlag.Converged

    for k in range(1,max_iter):
        # Try doing a quadratic step to get a next point x''; we calculate x4
        x4 = None  # Assume the quadratic step will fail
        denom = None
        steptype = "Qd"  # Quadratic step for log
        # YOUR CODE to set x4 for a quadratic step; put x4=None if the step is not valid
        # Check if we have 3 values for quadratic calculation

        if len(x1x2x3) == 3:
            denom = ((x1x2x3[1] - x1x2x3[0]) * (fx1x2x3[1] - fx1x2x3[2]) - (x1x2x3[1] - x1x2x3[2]) * (
                        fx1x2x3[1] - fx1x2x3[0]))
            if abs(denom) >= zerotol:
                x4 = x1x2x3[1] - 0.5 * (
                            (x1x2x3[1] - x1x2x3[0]) ** 2 * (fx1x2x3[1] - fx1x2x3[2]) - (x1x2x3[1] - x1x2x3[2]) ** 2 * (
                                fx1x2x3[1] - fx1x2x3[0])) / denom
                if x4 < a or x4 > b:
                    x4 = None

            # If quadratic step failed, use Brent's Golden Section style calculation
        xdd = x4
        if not xdd:
            steptype = "GS"
            if xd <= (a + b) / 2:
                xdd = a + (1 - tau) * (b - a)
            else:
                xdd = a + tau * (b - a)

        # xdd is now our new (Quadratic or Golden Section) point in [a,b]. Calc f(xdd), and do housekeeping.
        fdd = f(xdd)
        xlist.append(xdd)
        flist.append(fdd)
        logiteration(f, k, a, xd, xdd, b, x1x2x3, x4, denom, steptype, showlog)
        (oldxd,oldxdd)=(xd,xdd) # Save for logging

        # Now Update xd, a, b, fd (similar to Golden Section update) to shrink interval of uncertainty [a,b] around the better of x' and x''
        # Note: We must now test for xd < xdd (not x<a+b)/2) because we may have both xd<(a+b)/2 and xdd<(a+b)/2 if xdd comes from quadratic
        # We want xd to always be the better of xd and xdd (which will automatically be the best of x1, x2, x3)
        # YOUR CODE to update a, xd, b. This code should NOT refer to x1, x2, x3, x4

        # Update a, b, and xd
        if fdd <= fd:
            if xd <= xdd:
                b = xd
            else:
                a = xd
        else:
            if xd <= xdd:
                a = xdd
            else:
                b = xdd

        xd = xdd
        fd = fdd
        # Show the updated a, xd, b values in the log
        logstep(f, k, a, xd, oldxd, oldxdd, b, showlog)
        
        # Update x1..x3 by either (1) adding x4 if we don't already have 3 values,
        # or (2) by replacing the worst of x1..x3 with x4. (You can assume x4 is better than the worst of x1...x3)
        # YOUR CODE goes here

        # Update x1x2x3
        if len(x1x2x3) < 3:
            x1x2x3.append(xdd)
            fx1x2x3.append(fdd)
        else:
            i = np.argmax(fx1x2x3)
            x1x2x3[i] = xdd
            fx1x2x3[i] = fdd

        # Test for convergence
        if b-a<tol:
            logfinal(f, k, a, b, tol, showlog, ExitFlag.Converged)
            return [a,b], xlist, flist, k, ExitFlag.Converged

    # Exit having reached max iterations
    logfinal(f, k, a, b, tol, showlog, ExitFlag.MaxIterations)
    return [a,b], xlist, flist, k, ExitFlag.MaxIterations


def logiteration(f, k, a, xd, xdd, b, x1x2x3, x4, denom, steptype, showlog):
    if showlog:
        for j in range(len(x1x2x3)):
            print(f'{(k if j==0 else ""):2}  {color(x1x2x3[j])}x{j+1}={x1x2x3[j]:25.20f}{endcolor},  f{j+1}={f(x1x2x3[j]):25.20f}')
        if x4:
            print(f'    x{4}={color(x4)}{x4:25.20f}{endcolor},  f{4}={f(x4):25.20f}  {"x4<a" if x4<a else "x4>b" if x4>b else ""}')
        if denom:
            print(f' denom={denom:25.20f} {"=~= zero" if abs(denom)<zerotol else ""}')
        (alpha,beta,falpha,fbeta,n1,n2,n3,n4) = (xd,xdd,f(xd),f(xdd)," x'","x''"," f'","f''") if xd<xdd else (xdd,xd,f(xdd),f(xd),"x''"," x'","f''"," f'")
        print(f' {steptype}  {color(a)}a={a:25.20f}{"*" if falpha <= fbeta else " "} {color(alpha)}{n1}={alpha:25.20f}* {color(beta)}'
              f'{n2}={beta:25.20f}* {color(b)}b={b:25.20f}{"*" if falpha > fbeta else " "}{endcolor}   b-a= {b-a} ')
        print(f"                                  {n3}={falpha:25.20f}  {n4}={fbeta:25.20f}  ")
        if not (a<=alpha<=beta<=b): print("Warning: We do not have a<alpha<beta<b")


def logstep(f, k, a, xd, oldxd, oldxdd, b, showlog):
    if showlog:
        alpha = min(oldxd, oldxdd)
        if xd==alpha:
            print(f" =>  {color(a)}a={a:25.20f}   {color(xd)}x'={xd:25.20f}    {color(b)}b={b:25.20f}{endcolor}   {' ':25}     b-a= {b-a}")
        else:
            print(f" =>  {' ':25}      {color(a)}a={a:25.20f}   {color(xd)}x'={xd:25.20f}  {color(b)}b={b:25.20f}{endcolor}    b-a= {b-a}")
        if not (a<=xd<=b): print("Warning: We do not have a<alpha<beta<b")
        print()


def logfinal(f, k, a, b, tol, showlog, exitflag):
    if showlog:
        print(f'{k:2}   {color(a)}a={a:25.20f} {"":62} {color(b)}b={b:25.20f}{endcolor}    b-a= {b-a}{"< tol" if b-a<tol else ""}')
        # print(f"     f({(a+b)/2:25.20f})={f((a+b)/2):25.20f}")
        print(f"     f({(a+b)/2})={f((a+b)/2)}")
        if exitflag == ExitFlag.MaxIterations: print(f'     Iteration limit reached')
        if exitflag == ExitFlag.Converged: print(f'     Converged')


if __name__ == "__main__":
    from functions import allfunctions, allfunctiontitles
    from testoptimiser import testoptimiser

    # initialisation
    tol = 10e-4
    max_iter = 100
    a = -0.3   # a & b define uncertainty interval
    b = 3.0
    plotleft = -0.3 # plotleft & plotright define the plot range
    plotright = 3.0
    showlog = True

    testoptimiser(fullbrent,"Brents Full Method",  allfunctions, allfunctiontitles, a, b, max_iter, tol, showlog, plotleft, plotright)

