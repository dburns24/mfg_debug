

import random

from itertools import count

import pandas as pd

import matplotlib.pyplot as plt

from matplotlib.animation import FuncAnimation

import csv

plt.style.use('fivethirtyeight')

x_vals = []

y_vals = []



index = count()

fig = plt.figure()



def animate(i):
    data = pd.read_csv('-37.csv')
    #plt.ylim(0, 30)
 
    x1 = data['RF_FREQ']
    y1 = data['GAIN']   

    
    data = pd.read_csv('-33.csv')
    x2 = data['RF_FREQ']
    y2 = data['GAIN']
        
    
    data = pd.read_csv('-29.csv')
    x3 = data['RF_FREQ']
    y3 = data['GAIN']
        
    data = pd.read_csv('-25.csv')
    x4 = data['RF_FREQ']
    y4 = data['GAIN']
        
    
    data = pd.read_csv('-21.csv')
    x5 = data['RF_FREQ']
    y5 = data['GAIN']
        
    
    data = pd.read_csv('-17.csv')
    x6 = data['RF_FREQ']
    y6 = data['GAIN']
        
    
    data = pd.read_csv('-13.csv')
    x7 = data['RF_FREQ']
    y7 = data['GAIN']
        
    
    data = pd.read_csv('-9.csv')
    x8 = data['RF_FREQ']
    y8 = data['GAIN']
        
    
    plt.cla()
    #plt.plot(x, y1, label='Gain')
    plt.plot(x1, y1, label='-37dBm Input', color='green', linewidth=1)
    plt.plot(x2, y2, label='-33dBm Input', color='blue', linewidth=1)
    plt.plot(x3, y3, label='-29dBm Input', color='red', linewidth=1)
    plt.plot(x4, y4, label='-25dBm Input', color='gray', linewidth=1)
    plt.plot(x5, y5, label='-21dBm Input', color='orange', linewidth=1)
    plt.plot(x6, y6, label='-17dBm Input', color='cyan', linewidth=1)
    plt.plot(x7, y7, label='-13dBm Input', color='black', linewidth=1)
    plt.plot(x8, y8, label='-9dBm Input', color='purple', linewidth=1)


    plt.legend(loc='upper left', prop={'size': 8})
    plt.title('Tx Gain', fontdict={'fontsize':13})
    plt.xlabel('Ch FREQ (GHz)', fontsize=9)
    plt.ylabel('GAIN (dB)', fontsize=9)
    #plt.xticks( rotation=45)
    plt.tick_params(labelsize = 8)



ani = FuncAnimation(plt.gcf(), animate, interval=1000)



#plt.tight_layout()

plt.show()

fig.savefig("Gain.png")


