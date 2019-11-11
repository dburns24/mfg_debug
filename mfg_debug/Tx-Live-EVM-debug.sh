#!/bin/bash

echo plotting Tx Gain in real time
python3 Tx-EVM-min-Live-context.py &


#python3 ./2x2_fig2_plot.py &
python3 ./Ch0_2x2_fig1_plot.py &
python3 ./Ch0_2x2_fig2_plot.py &
#python3 ./Ch1_2x2_fig1_plot.py &
#python3 ./Ch1_2x2_fig2_plot.py &
#python3 ./Ch2_2x2_fig1_plot.py &
#python3 ./Ch2_2x2_fig2_plot.py &
#python3 ./Ch3_2x2_fig1_plot.py &
#python3 ./Ch3_2x2_fig2_plot.py &

clear
