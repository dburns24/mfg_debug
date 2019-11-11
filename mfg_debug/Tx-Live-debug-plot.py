
# https://matplotlib.org/3.1.0/gallery/subplots_axes_and_figures/subplots_demo.html

import random

from itertools import count

import pandas as pd
import numpy as np

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

ax.figure.set_facecolor("grey")

index = count()

def animate(i):
    
    data = pd.read_csv('dataTxGain1.csv')
    RF_FREQ = data['RF_Freq']
    Gain = data['Gain']

    plt.cla()     # this line is for redrawing
     
    ax.plot(RF_FREQ, Gain, color="orange", label='Gain',linewidth=1.5)
    ax.set_title("Tx_Gain (A Few Overlay Plots)")
    ax.set_ylabel("Gain (dB)")
    ax.set_xlabel("Ch Freq (GHz)")
    #ax.set_ylim([-40, 35])
    ax.set_xlim([34.1, 43.9])
    ax.axvline(x=37.1, ymin=-40, ymax=18, color='r', linestyle='--', alpha=1)
    ax.axvline(x=39.9, ymin=-40, ymax=18, color='r', linestyle='--', alpha=1)
    #plt.show()
    
    
    data1 = pd.read_csv('dataTxGain2.csv')
    RF_FREQ1 = data1['RF_Freq']
    Gain1 = data1['Gain']
    ax.plot(RF_FREQ1, Gain1, color="yellow", label='Gain',linewidth=1.5)
    
    
    data2 = pd.read_csv('dataTxGain3.csv')
    RF_FREQ2 = data2['RF_Freq']
    Gain2 = data2['Gain']
    ax.plot(RF_FREQ2, Gain2, color="purple", label='Gain',linewidth=1.5)
    
    fig.savefig('Few_Tx_Gain_Plots.png', facecolor=fig.get_facecolor())
    

ani = FuncAnimation(plt.gcf(), animate, interval=10)


#plt.tight_layout()
plt.show()






