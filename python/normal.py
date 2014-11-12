from __future__ import absolute_import
from __future__ import print_function
import numpy as np
from matplotlib import pyplot as plt
import matplotlib as mpl
mpl.rcParams['font.size'] = 16

def plot(mu, sigma, x, color='k'):
    fac = 1.0/np.sqrt(2*np.pi)/sigma
    y = fac*np.exp(-(x-mu)**2/2/sigma**2)
    plt.plot(x, y, color=color, lw = 2)
    return fac

if __name__ == '__main__':
    x = np.linspace(-3.5, 5.5, 500)
    my = plot(0, 1.0, x)
    plt.annotate(r'$\sigma=1$', xy = (0, my), xytext = (-2.0, my+0.08),
                 arrowprops = dict(facecolor='black', width=0.5))
    my = plot(0, 2.0, x)
    plt.annotate(r'$\sigma=2$', xy = (0, my), xytext = (-2.0, my+0.08),
                 arrowprops = dict(facecolor='black', width=0.5))
    my = plot(0, 0.5, x)
    plt.annotate(r'$\sigma=0.5$', xy = (0, my), xytext = (-2.0, my+0.08),
                 arrowprops = dict(facecolor='black', width=0.5))

    plot(4.0, 1.0, x, color='r')
    plot(4.0, 2.0, x, color='r')
    plot(4.0, 0.5, x, color='r')

    plt.axvline(x=0)
    plt.axhline(y=0)
    
    plt.axis([-3.5, 5.5, 0, 1])
    plt.savefig('normal_musigma.pdf')
    plt.show()
