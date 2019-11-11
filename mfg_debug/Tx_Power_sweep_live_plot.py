

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
    
    data = pd.read_csv('data_P1dB.csv')
    plt.ylim(0, 30)
    
    x1 = data['IF_INPUT']
    y1 = data['OUTPUT_POWER_37p1']
    y2 = data['OUTPUT_POWER_37p3']
    y3 = data['OUTPUT_POWER_37p5']
    y4 = data['OUTPUT_POWER_37p7']
    y5 = data['OUTPUT_POWER_37p9']
    
    y6 = data['OUTPUT_POWER_38p1']
    y7 = data['OUTPUT_POWER_38p3']
    y8 = data['OUTPUT_POWER_38p5']
    y9 = data['OUTPUT_POWER_38p7']
    y10 = data['OUTPUT_POWER_38p9']
    y11 = data['OUTPUT_POWER_39p1']
    y12 = data['OUTPUT_POWER_39p3']
    y13 = data['OUTPUT_POWER_39p5']
    y14 = data['OUTPUT_POWER_39p7']
    y15 = data['OUTPUT_POWER_39p9']

    plt.cla()



    #plt.plot(x, y1, label='Gain')
    plt.plot(x1, y1, label='37.1G', color='green', linewidth=1)
    plt.plot(x1, y2, label='37.3G', color='blue', linewidth=1)
    plt.plot(x1, y3, label='37.5G', color='red', linewidth=1)
    plt.plot(x1, y4, label='37.7G', color='gray', linewidth=1)
    plt.plot(x1, y5, label='37.9G', color='orange', linewidth=1)
    
    plt.plot(x1, y6, label='38.1G', color='cyan', linewidth=1)
    plt.plot(x1, y7, label='38.3G', color='black', linewidth=1)
    plt.plot(x1, y8, label='38.5G', color='purple', linewidth=1)
    plt.plot(x1, y9, label='38.7G', color='magenta', linewidth=1)
    plt.plot(x1, y10, label='38.9G', color='yellow', linewidth=1)
    
    plt.plot(x1, y11, label='39.1G', color='pink', linewidth=1)
    plt.plot(x1, y12, label='39.3G', color='olive', linewidth=1)
    plt.plot(x1, y13, label='39.5G', color='brown', linewidth=1)
    plt.plot(x1, y14, label='39.7G', color='gold', linewidth=1)
    plt.plot(x1, y15, label='39.9G', color='lime', linewidth=1)
    
    plt.legend(loc='upper left', prop={'size': 8})
    plt.title('Power Sweep', fontdict={'fontsize':13})
    plt.xlabel('IF Input (dBm)', fontsize=9)
    plt.ylabel('OUTPUT_POWER (dBm)', fontsize=9)
    #plt.xticks( rotation=45)
    plt.tick_params(labelsize = 8)
    



ani = FuncAnimation(plt.gcf(), animate, interval=1000)



#plt.tight_layout()

plt.show()

fig.savefig("Power_Sweep.png")

