#!/bin/bash

echo plotting Tx Gain in real time
python3 Tx-Live-debug-3-color-traces.py &


python3 ./Tx-Live-debug-plots-overlay.py &
python3 ./Tx-Live-debug-plot.py &
clear
