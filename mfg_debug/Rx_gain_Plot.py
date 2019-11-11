

import random

from itertools import count

import pandas as pd

import matplotlib.pyplot as plt

from matplotlib.animation import FuncAnimation

import csv

plt.style.use('fivethirtyeight')

x_vals = []

y_vals = []
'''
fieldnames = ["RF_Freq", "Gain"]
with open('dataRxGain.csv', 'w') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    csv_writer.writeheader()
'''   
plt.style.use('seaborn')

index = count()

fig = plt.figure()



def animate(i):
    
    
    data = pd.read_csv('dataRxGain.csv')

    x1 = data['RF_Freq']

    y1 = data['Gain']
    plt.autoscale(enable=False, axis='y')
     
    plt.set_ylim([0, 15])
    
    plt.cla()



    #plt.plot(x, y1, label='Gain')
    #plt.plot(x1, y1, label='37.1G', color='green', linewidth=1)

    plt.plot(x1, y1, color='green', linewidth=1)
    plt.legend(loc='upper left', prop={'size': 8})
    plt.title('Rx Gain', fontdict={'fontsize':13})
    plt.xlabel('Ch. Freq (GHz)', fontsize=9)
    plt.ylabel('Gain (dB)', fontsize=9)
    #plt.xticks( rotation=45)
    plt.tick_params(labelsize = 8)
    



ani = FuncAnimation(plt.gcf(), animate, interval=1000)



#plt.tight_layout()

plt.show()

fig.savefig("Rx_gain.png")


