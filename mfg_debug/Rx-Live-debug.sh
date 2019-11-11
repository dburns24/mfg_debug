#!/bin/bash

echo plotting Rx Gain in real time
python3 Rx-Live-debug-3-color-traces.py &


python3 ./Rx-Live-debug-plots-overlay.py &
python3 ./Rx-Live-debug-plot.py &
clear
