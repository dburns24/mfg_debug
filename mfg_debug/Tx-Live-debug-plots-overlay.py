
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
with open('dataTxGain.csv', 'w') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    csv_writer.writeheader()
''' 
plt.style.use('seaborn')
plt.style.use('dark_background')

fig, ax = plt.subplots()
ax.figure.set_facecolor("brown")

index = count()

def animate(i):
    data = pd.read_csv('dataTxGain.csv')

    RF_FREQ = data['RF_Freq']

    Gain = data['Gain']

    plt.cla()       #  this line will redraw 

    print("----------------", RF_FREQ)

    ax.plot(RF_FREQ, Gain, color = "yellow", label='Gain', linewidth=1.5)
    
    ax.set_title("Tx_Gain (Overlay Plots)")
    ax.set_ylabel("Gain (dB)")
    ax.set_xlabel("Ch Freq (GHz)")
    #ax.set_ylim([-40, 35])
    ax.set_xlim([34.1, 43.9])
    
    #ax1.axhline(y=0.5, xmin=0.0, xmax=1.0, color='k', linestyle='--', alpha=0.3)
    #plt.axvline(x=0.306, ymin=0, ymax = 1, linewidth=2, color='r')
    ax.axvline(x=37.1, ymin=-40, ymax=18, color='r', linestyle='--', alpha=1)
    ax.axvline(x=39.9, ymin=-40, ymax=18, color='r', linestyle='--', alpha=1)
    #ax.set_facecolor("black")
    #plt.show()
    fig.savefig('Overlay_Tx_Gain_Plots.png', facecolor=fig.get_facecolor())
    
ani = FuncAnimation(plt.gcf(), animate, interval=10)

#plt.tight_layout()
plt.show()





