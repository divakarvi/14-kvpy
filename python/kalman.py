from __future__ import absolute_import
from __future__ import print_function
import numpy as np
import os

def gen_kalman_data(n = 1000, sigma = 1.0):
    fname = '../data/kalman_n{0:d}_s{1:.1f}.npz'.format(n, sigma)
    if os.path.isfile(fname):
        print('data already there')
        return

    x = np.zeros(n, dtype = float)
    y = np.zeros(n, dtype = float)
    z = np.zeros(n, dtype = float)

    theta = np.random.uniform(0.0, 2*np.pi)
    x[0] = np.cos(theta)
    y[0] = np.sin(theta)

    for i in range(1, n):
        x[i] = (x[i-1] - y[i-1])/np.sqrt(2.0)
        y[i] = (x[i-1] + y[i-1])/np.sqrt(2.0)

    #noisy observations
    for i in range(n):
        z[i] = y[i] + np.random.normal(scale = sigma)
        
    fname = '../data/kalman_n{0:d}_s{1:.1f}'.format(n, sigma)
    np.savez(fname, x = x, y = y, z = z)

def load_data(n, sigma):
    fname = '../data/kalman_n{0:d}_s{1:.1f}.npz'.format(n, sigma)
    data = np.load(fname)
    x = data['x']
    y = data['y']
    z = data['z']
    return x, y, z

def kalman_filter(z, sigma):
    n = z.size
    
    x = np.zeros(n, dtype = float)
    y = np.zeros(n, dtype = float)
    a = np.zeros(n, dtype = float)
    b = np.zeros(n, dtype = float)
    c = np.zeros(n, dtype = float)

    xn = 0.0 #initialize filter state, this is arbitrary
    yn = 0.0 #n for now 
    an = 0.3
    bn = 0.2
    cn = 0.3
    assert an*cn >= bn**2

    for i in range(n):
        #propagate to next step
        x[i] = (xn - yn)/np.sqrt(2.0)
        y[i] = (xn + yn)/np.sqrt(2.0)
        a[i] = (an + cn)/2.0 - bn
        b[i] = (an - cn)/2.0
        c[i] = (an + cn)/2.0 + bn
        assert a[i]*c[i] >= b[i]**2

        #incorporate observation z[i]
        c[i] = c[i] + 1.0/(2.0*sigma**2)
        z[i] = z[i] - y[i]
        #note c[i] has been updated
        alpha = b[i]*(z[i]/sigma**2)/(b[i]**2 - a[i]*c[i])
        beta = -a[i]*(z[i]/sigma**2)/(b[i]**2 - a[i]*c[i])
        x[i] = x[i] + alpha
        y[i] = y[i] + beta

        #prepare for next iteration
        xn = x[i]
        yn = y[i]
        an = a[i]
        bn = b[i]
        cn = c[i]

    return x, y


if __name__ == '__main__':
    n = 1000
    sigma = 1.0
    gen_kalman_data(n, sigma)
    x, y, z = load_data(n, sigma)

    yno = raw_input('Save figures? y/n:')

    from matplotlib import pyplot as plt
    m = 50
    plt.plot(x[:m], '--ko')
    plt.plot(y[:m], '--bo')
    plt.plot(z[:m], '--go')
    plt.legend(['x','y','z'])
    plt.xlabel('n')
    plt.ylabel('x,y,z')
    if yno == 'y':
        plt.savefig('signal.pdf')
    plt.show()

    xx, yy = kalman_filter(z, sigma)



    plt.plot(y-yy)
    plt.xlabel('n')
    plt.ylabel('Error in estimated y')
    plt.show()
    plt.plot(x-xx)
    plt.xlabel('n')
    plt.ylabel('Error in estimated x')
    plt.show()
    plt.plot(y[-m:], '--bo')
    plt.plot(yy[-m:], '--go')
    plt.legend(['y', 'estimated y'])
    plt.xlabel('n - ' + str(y.size - m))
    plt.ylabel('y, estimated y')
    if yno == 'y':
        plt.savefig('yest.pdf')
    plt.show()
    plt.plot(x[-m:], '--bo')
    plt.plot(xx[-m:], '--go')
    plt.legend(['x', 'estimated x'])
    plt.xlabel('n - ' + str(x.size - m))
    plt.ylabel('x, estimated x')
    if yno == 'y':
        plt.savefig('xest.pdf')
    plt.show()
