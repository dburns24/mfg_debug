#!/bin/bash
i = 0
#do 


echo plotting Rx Gain in real time
python3 Relay-EVT3-Rx-Live-noline.py &
#sleep 2
#python3 ./Rx_gain_Plot.py &

python3 ./sca.py &
python3 ./sca_overwrite.py &




clear
#done