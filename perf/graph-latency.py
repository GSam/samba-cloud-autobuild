#!/usr/bin/python
import matplotlib
import matplotlib.pyplot as plt
import sys
import os
from math import exp

def plot_n_squared(ax, n, scale):
    seq = [(i * scale) ** 2 for i in range(n) ]
    ax.plot(seq, 'k-', linewidth=1, label='(n * %g) ^ 2' % scale)
    

def plot_exp_n(ax, n, scale):
    seq = [exp(i * scale)for i in range(n) ]
    ax.plot(seq, 'k:', linewidth=1, label='exp(n * %g)' % scale)
    

def plot(sequences, keys):
    ax = plt.subplot(1, 1, 0)
    
    for c, s, k in zip('rgby', sequences, keys):
        ax.plot(s, '%s.' % c, linewidth=0.5, label=k)
    return ax
    
def main():
    keys=None
    rows = []
    f = open(sys.argv[1])
    print f, sys.argv
    for line in f:
        try:
            rows.append([float(x) for x in line.split()])
        except ValueError, e:
            if line[:5] == 'KEYS:':
                keys = line[5:].split()
            print line, e

    f.close()
    
    sequences = zip(*rows)
    ax = plot(sequences, keys)
    #plot_n_squared(ax, len(rows), 5.6e-5)
    #plot_exp_n(ax, len(rows), 5e-5)

    plt.grid(True)
    plt.legend(loc='upper left', numpoints=1, frameon=False, borderpad=0)    
    plt.show()
    

main()
