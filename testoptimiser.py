import numpy as np
import matplotlib.pyplot as plt

# Inputs
# optimiser     The optimisation algorithm to be tested that does the minimisation 
# optimisername The name of this optimisation algorithm to output
# functions     A list of functions to be used during the testing
# ftitles       The titles of these functions
# [a, b]        initial interval of uncertainty
# max_iter      maximum number of iterations performed
# tol           requred interval of uncertainty
# showlog       True to output detailed steps
# plotleft      The minimum x for the ploit
# plotright     The maximum x for the ploit


def testoptimiser(optimiser,optimisername, functions, ftitles, a, b, max_iter, tol, showlog, plotleft, plotright):
    plt.rcParams['figure.constrained_layout.use'] = True
    fig, ax = plt.subplots(nrows=3,ncols=len(functions))

    for i in range(len(functions)):
        f = functions[i]                # The function to minmise
        ftitle = ftitles[i]             # The Latext plot title for the function
        fname = functions[i].__name__   # Get the Python function name, eg f0

        x=np.linspace(plotleft,plotright,100)
        ax[0,i].plot(x, [f(x1) for x1 in x], zorder=10)
        ax[0,i].set_title(ftitle)
        ax[0,i].set_xlabel('$x$')
        ax[0,i].set_ylabel('$f_{'+fname[1:]+'}(x)$')
        
        print(f'Running {optimisername} applied to {fname}...')
        result, xlist, flist, k, exit_flag = optimiser(f, [a, b], max_iter, tol, showlog)
        print(f'{optimisername} applied to {fname} returned {result} after {k} iterations; flag={exit_flag}')
        
        ax[0,i].scatter(xlist, flist, zorder=11)
        ax[0,i].scatter(xlist[-1],flist[-1], zorder=12)       
        ax[0,i].grid(True)

        ax[1,i].scatter(range(len(flist)),flist, zorder=10)
        ax[1,i].set_xlabel('$k$')
        ax[1,i].set_ylabel('$f_{'+fname[1:]+'}(x^{(k)})$')
        ax[1,i].grid(True)

        ax[2,i].scatter(range(len(flist)),xlist, zorder=10)
        ax[2,i].set_xlabel('$k$')
        ax[2,i].set_ylabel('$x^{(k)}$')
        ax[2,i].grid(True)
        
        # For older versions of MatplotLib:         fig.canvas.set_window_title('Brent\'s method') 
        fig.canvas.manager.set_window_title(optimisername) 

    plt.show()
