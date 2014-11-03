from __future__ import absolute_import
from __future__ import print_function
import numpy as np

def get_pearson_data():
    import os
    assert os.path.isfile('../data/Pearson.txt')
    data = np.loadtxt('../data/Pearson.txt', comments = '#')
    data = data[:,0] #discard sons
    mean = np.mean(data)
    sigma = np.std(data)#sigma**2 = variance, sigma = std deviation
    return data, mean, sigma

def normal_law(x, mean, sigma):
    y = x - mean
    return 1.0/np.sqrt(2.0*np.pi)/sigma * np.exp(-y*y/2.0/sigma**2)
  
if __name__ == '__main__':  
    data, mean, sigma = get_pearson_data()
    print('number of items = ', data.size)
    print('        minimum = ', min(data))
    print('        maximum = ', max(data))
    print('           mean = ', mean)
    print('            std = ', sigma)
    from matplotlib import pyplot as plt
    bins = np.linspace(min(data), max(data), 16)
    plt.hist(data, bins = bins)
    
    x = np.linspace(min(data), max(data), 500)
    nml = normal_law(x, mean, sigma)
    #scale to compare
    #area under curve = area under histogram = data.size * (bins[1] - bins[0])
    nml = nml * data.size*(bins[1] - bins[0]) 
    plt.plot(x, nml, 'k', lw = 5) 
    plt.xlabel('Height in Inches')
    x = raw_input('save figure? y/n:')
    if x == 'y':
        plt.savefig('heights.pdf')
    plt.show()

    
