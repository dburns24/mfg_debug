#!/bin/bash

while:

do
	echo "Press [CTRL+C] to stop.."
	python3.7 ./Rx_fig1_plot.py &
	echo plotting Rx Gain in real time
	python3.7 Relay-EVT3-Rx-Live.py &

done