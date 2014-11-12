#!/usr/bin/env python
from __future__ import absolute_import
from __future__ import print_function
import numpy as np

def normal_plot(mu, sigma):
    x = np.linspace(mu-3*sigma, mu+3*sigma, 250)
    y = 1.0/(np.sqrt(2*np.pi)*sigma)*np.exp(-(x-mu)**2/2.0/sigma**2)
    from matplotlib import pyplot as plt
    plt.plot(x, y, 'k', lw = 3)
    ymax = max(y)
    dx = np.sqrt(2.0*np.log(2.0))*sigma
    xx = np.linspace(mu- dx, mu + dx, 100)
    plt.plot(xx, ymax/2.0*np.ones(xx.size), 'k', lw = 3) 
    plt.axis('off')
    plt.savefig('normal1d.svg')
    plt.show()

def normal_plot2d():
    mux = 3.0
    muy = 3.0
    sigmax = 1.0
    sigmay = 0.5

    x = np.linspace(mux - 3*sigmax, mux + 3*sigmax, 25)
    y = np.linspace(muy - 3*sigmay, muy + 3*sigmay, 25)
    X,Y = np.meshgrid(x, y)

    f = 1.0/np.sqrt(2.0*np.pi)
    Z = (f/sigmax)*(f/sigmay)*np.exp(-(X-mux)**2/2.0/sigmax**2
                                     -(Y-muy)**2/2.0/sigmay**2)

    from mpl_toolkits.mplot3d import Axes3D
    from matplotlib import pyplot as plt
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.plot_wireframe(X, Y, Z, rstride = 1, cstride = 1, color = 'k')

    t = np.linspace(0, 2*np.pi, 100)
    x = mux + sigmax*np.sqrt(2.0*np.log(2.0))*np.cos(t)
    y = muy + sigmay*np.sqrt(2.0*np.log(2.0))*np.sin(t)
    print(Z.max())
    ax.plot(x, y, Z.max()/2.0, lw = 4, color = 'r')

    plt.axis('off')
    plt.savefig('normal2d.svg')
    plt.show()

def rotate_ellipse():
    from matplotlib import pyplot as plt
    
    mux = 1.0
    muy = 0.0
    sigmax = 0.5
    sigmay = 0.3

    t = np.linspace(0, 2*np.pi, 100)
    x = mux + sigmax*np.sqrt(2.0*np.log(2.0))*np.cos(t)
    y = muy + sigmay*np.sqrt(2.0*np.log(2.0))*np.sin(t)

    plt.plot(x, y, '--r', lw = 2)
    
    xx = (x - y)/np.sqrt(2.0)
    yy = (x + y)/np.sqrt(2.0)
    plt.plot(xx, yy, 'r', lw = 2)

    plt.axis([-2, 2, -2, 2])
    plt.axhline()
    plt.axvline()
    plt.axis('off')
    plt.savefig('rotate.pdf')

    plt.show()

def noisy_observation(stage):
    assert stage == 'noisy' or stage == 'section'

    from mpl_toolkits.mplot3d import Axes3D
    from matplotlib import pyplot as plt
    
    mux = 1.0
    muy = 0.0
    sigmax = 0.5*np.sqrt(2.0*np.log(2.0))
    sigmay = 0.3*np.sqrt(2.0*np.log(2.0))

    t = np.linspace(0, 2*np.pi, 100)
    x = mux + sigmax*np.cos(t)
    y = muy + sigmay*np.sin(t)
    fig = plt.figure()
    ax = fig.gca(projection = '3d')
    plt.plot(x, y, '--r', lw = 2, zorder = 1)


    xx = (x - y)/np.sqrt(2.0)
    muxx = (mux - muy)/np.sqrt(2.0)
    yy = (x + y)/np.sqrt(2.0)
    muyy = (mux + muy)/np.sqrt(2.0)
    #plt.plot(xx, yy, 'r', lw = 2)

    n = 20
    sz = x.size
    xxx = np.zeros(sz*n)
    yyy = np.zeros(sz*n)
    eta = np.zeros(sz*n)
    seta = sigmay
    scl = np.linspace(0.9999, 1.0/n, n)
    for i in range(n):
        xxx[sz*i:sz*(i+1)] = muxx+scl[i]*(xx - muxx)
        yyy[sz*i:sz*(i+1)] = muyy+scl[i]*(yy - muyy)
        eta[sz*i:sz*(i+1)] = seta*np.sqrt(1.0
                                          -(scl[i]*(x-mux))**2/sigmax**2
                                          -(scl[i]*(y-muy))**2/sigmay**2)
    ax.plot_trisurf(xxx, yyy, eta, color='r', zorder=2)

    
    ax.set_xlim(-0.5, 1.5)
    ax.set_ylim(-0.5, 1.5)
    ax.set_zlim(0, 1.5)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel(r'$\eta$')
    plt.setp( ax.get_xticklabels(), visible=False)
    plt.setp( ax.get_yticklabels(), visible=False)
    plt.setp( ax.get_zticklabels(), visible=False)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])

    if stage == 'noisy':
        plt.savefig('add_noise.pdf')
        plt.show()


    x = np.linspace(xx.min()+0.2, xx.max()-0.2, 20)
    y = np.linspace(yy.min(), yy.max(), 20)
    X, Y = np.meshgrid(x, y)
    z = muyy + 0.02
    Eta = Y - z
    ax.plot_wireframe(X, Y, Eta, zorder=3)
    plt.savefig('section.pdf')
    plt.show()

if __name__ == '__main__':
    #rotate_ellipse()
    noisy_observation('section')
