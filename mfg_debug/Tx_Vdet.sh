#!/bin/bash


#To make sure it is executable, type:

#chmod +x myscript.sh

#And to run it, type:

#     ./myscript.sh

#echo plotting V_Det vs Output_Power in real time
python3 ./Tx_Vdet_live_plot.py &


#echo plotting Log V_Det vs Output_Power in real time
python3 ./Tx_Log_Vdet_live_plot.py &


echo plotting Tx Power Sweep in real time
python3 ./Tx_Power_sweep_live_plot.py &

#echo plotting Tx Gain in real time
python3 ./Tx_Gain_live_plot.py &

python3 ./Tx-Vdet-live.py &
python3 ./Tx-live.py &






