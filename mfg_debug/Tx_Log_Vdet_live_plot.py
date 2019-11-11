

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
    
    data = pd.read_csv('data_V_Det.csv')

    x1 = data['OUTPUT_POWER_37p1']
    y1 = data['L_PWR_DET_37p1']

    x2 = data['OUTPUT_POWER_37p3']
    y2 = data['L_PWR_DET_37p3']
    
    x3 = data['OUTPUT_POWER_37p5']
    y3 = data['L_PWR_DET_37p5']
    
    x4 = data['OUTPUT_POWER_37p7']
    y4 = data['L_PWR_DET_37p7']
    
    x5 = data['OUTPUT_POWER_37p9']
    y5 = data['L_PWR_DET_37p9']
    
    x6 = data['OUTPUT_POWER_38p1']
    y6 = data['L_PWR_DET_38p1']
    
    x7 = data['OUTPUT_POWER_38p3']
    y7 = data['L_PWR_DET_38p3']
    
    x8 = data['OUTPUT_POWER_38p5']
    y8 = data['L_PWR_DET_38p5']
    
    x9 = data['OUTPUT_POWER_38p7']
    y9 = data['L_PWR_DET_38p7']    
    
    x10 = data['OUTPUT_POWER_38p9']
    y10 = data['L_PWR_DET_38p9']

    x11 = data['OUTPUT_POWER_39p1']
    y11 = data['L_PWR_DET_39p1']
    
    x12 = data['OUTPUT_POWER_39p3']
    y12 = data['L_PWR_DET_39p3']
    
    x13 = data['OUTPUT_POWER_39p5']
    y13 = data['L_PWR_DET_39p5']
    
    x14 = data['OUTPUT_POWER_39p7']
    y14 = data['L_PWR_DET_39p7']
    
    x15 = data['OUTPUT_POWER_39p9']
    y15 = data['L_PWR_DET_39p9']   
    
    
    


    plt.cla()



    #plt.plot(x, y1, label='Gain')
    plt.plot(x1, y1, label='37.1G', color='green', linewidth=1)
    plt.plot(x2, y2, label='37.3G', color='blue', linewidth=1)
    plt.plot(x3, y3, label='37.5G', color='red', linewidth=1)
    
    plt.plot(x4, y4, label='37.7G', color='gray', linewidth=1)
    plt.plot(x5, y5, label='37.9G', color='orange', linewidth=1)
    plt.plot(x6, y6, label='38.1G', color='cyan', linewidth=1)
    
    
    plt.plot(x7, y7, label='38.3G', color='black', linewidth=1)
    plt.plot(x8, y8, label='38.5G', color='purple', linewidth=1)
    plt.plot(x9, y9, label='38.7G', color='magenta', linewidth=1)
    
    plt.plot(x10, y10, label='38.9G', color='yellow', linewidth=1)
    plt.plot(x11, y11, label='39.1G', color='pink', linewidth=1)
    plt.plot(x12, y12, label='39.3G', color='olive', linewidth=1)
    
    plt.plot(x13, y13, label='39.5G', color='brown', linewidth=1)
    plt.plot(x14, y14, label='39.7G', color='gold', linewidth=1)
    plt.plot(x15, y15, label='39.9G', color='lime', linewidth=1)
    
 
    plt.legend(loc='upper left', prop={'size': 8})
    plt.title('V_Det vs. Tx_Output_Power (Log-Log)', fontdict={'fontsize':13})
    plt.xlabel('Output Power (dBm)', fontsize=9)
    plt.ylabel('V_Det (dB)', fontsize=9)
    #plt.xticks( rotation=45)
    plt.tick_params(labelsize = 8)




ani = FuncAnimation(plt.gcf(), animate, interval=1000)



plt.tight_layout()

plt.show()

fig.savefig('Log_V_Det.png')

