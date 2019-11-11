
# https://matplotlib.org/3.1.0/gallery/subplots_axes_and_figures/subplots_demo.html

import random

from itertools import count

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

from matplotlib.animation import FuncAnimation

import csv

#plt.style.use('fivethirtyeight')

'''
fieldnames = ["RF_Freq", "Gain"]
with open('dataRxGain.csv', 'w') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    csv_writer.writeheader()
''' 
plt.style.use('seaborn')
plt.style.use('dark_background')

fig, ax = plt.subplots()
ax.figure.set_facecolor("green")

index = count()

def animate(i):
    data = pd.read_csv('dataRxGain.csv')

    RF_FREQ = data['RF_Freq']

    Gain = data['Gain']
    '''
    number_of_colors = 8
    color = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
                 for i in range(number_of_colors)]
    print(color)
    plt.scatter(random.randint(0, 10), random.randint(0,10), c=color[i], s=200)
    #plt.cla()
    ax.plot(RF_FREQ, Gain, c=color[i], label='Gain')
    '''
    plt.cla()       #  this line will redraw 

    print("----------------", RF_FREQ)
    #markers_on = [37.1, 38.5, 39.9]
    ax.plot(RF_FREQ, Gain, color = "yellow", label='Gain', linewidth=1.5)
    
    ax.set_title("Ch3 Rx_Gain (Overlay Plots)")
    ax.set_ylabel("Gain (dB)")
    ax.set_xlabel("Ch Freq (GHz)")
    ax.set_ylim([-40, 18])
    ax.set_xlim([24.1, 29.4])
    
    #ax1.axhline(y=0.5, xmin=0.0, xmax=1.0, color='k', linestyle='--', alpha=0.3)
    #plt.axvline(x=0.306, ymin=0, ymax = 1, linewidth=2, color='r')
    ax.axvline(x=37.1, ymin=-40, ymax=18, color='r', linestyle='--', alpha=1)
    ax.axvline(x=39.9, ymin=-40, ymax=18, color='r', linestyle='--', alpha=1)
    #ax.set_facecolor("black")
    #plt.show()
    fig.savefig('Overlay_Rx_Gain_Plots.png', facecolor=fig.get_facecolor())
    
ani = FuncAnimation(plt.gcf(), animate, interval=10)

#plt.tight_layout()
plt.show()




