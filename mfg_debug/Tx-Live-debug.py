# For Relay Rx TOI    2-26-2019       Wilson


"""
Created on Sat May 18 18:15:32 2019

@author: wfok

Must run "python Tx_set_EVT2.py off" & "python Tx_set_EVT2.py ch2" or include the script in below.

"""
import smbus
import time
import sys
import math
import RPi.GPIO as GPIO
import i2c
import temp
import cpld_stats
import cpld_adc_set
import subprocess
import stats
import pyvisa
import numpy as np
import time
from time import sleep
import csv
import os
import string
import visa


rm = visa.ResourceManager()
rm.list_resources()

SIGGEN_1 = rm.open_resource('TCPIP::10.12.117.104::INSTR')

#print(SIGGEN_1.query("*IDN?"))

SIGGEN_LO = rm.open_resource('TCPIP::10.12.116.61::INSTR')
#print(SIGGEN_LO.query("*IDN?"))

print(rm.list_resources())

SPECAN = rm.open_resource('TCPIP::10.12.116.8::INSTR')
print (SPECAN.query('*IDN?')) # Query the Identification string


fmt = "%Y-%m-%d %H-%M-%S"
t = time.strftime(fmt)
print("Timestamp Start = ", t)



SPECAN.write_termination = '\n'
SPECAN.write_termination = ''
SPECAN.write('*RST;*CLS') # Reset the instrument, clear the Error queue
SPECAN.write('INIT:CONT OFF') # Switch OFF the continuous sweep
SPECAN.write('SYST:DISP:UPD ON') # Display update ON - switch OFF after debugging
#SPECAN.ext_error_checking() # Error Checking after Initialization 

#SIGGEN_1.write('*RST')    
#SIGGEN_LO.write('*RST')   
SIGGEN_1.write(':OUTPut:MODulation:STATe OFF')                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
SIGGEN_1.write(':OUTPut:STATe ON')                    
SIGGEN_LO.write(':OUTPut:MODulation:STATe OFF')       
SIGGEN_LO.write(':OUTPut:STATe ON')                   
SIGGEN_LO.write(':FREQ:REF:STAT ON') 

Start = time.strftime(fmt)
print("Timestamp Start = ", Start)

Qorvo_temp_degC = 0
M1_temp_degC=0

LO_Path_Loss = 0.5    #  10 ft cable = 12dB loss, direct = 0.5dB loss
IF_Output_Path_Loss = 2        #9   for Tx and add 30dB or 58.5dB loss for Rx since this siggen could not go down below -20dBm   
RF_Input_Path_Loss = 30.5       #66.5
'''
Board_Type = input ("Enter Board Type: ")
Board_Type = str(Board_Type)
Board_SN = input ("Enter Board Serial Number: ")
Board_SN = str(Board_SN)   
Temperature = input ("Enter Temperature: ")
Temperature = str(Temperature)    
Chain_Num = input ("Enter Chain Number (make sure to connect the correct RF & IF ports): ")
Chain_Num = str(Chain_Num)
State = input ("Enter Tx or Rx state: ")
State = str(State)
Path = input ("Enter Gain path: ")
Path = str(Path)

'''
Board_Type = "EVT4_TTM_Case2"
Board_SN =  "1940060001"
Temperature = "25"    
Path = "3"
Polarization = " "
State = "Rx"
mode = "gain"

Chains = [3]
#Chains = [0]

fieldnames = ["RF_Freq", "Gain"]
with open('dataRxGain.csv', 'w') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    csv_writer.writeheader()

fieldnames1 = ["RF_Freq", "Gain"]
with open('dataRxGain1.csv', 'w') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames1)
    csv_writer.writeheader()

subprocess.run('python3 ./Rx_set.py gain', shell=True)
x = 0
n = 0
m = 0
while x==0:
    
    for Chain_Num in Chains:

            #IF_FREQ_RANGES = [5.25, 5.57]
            IF_FREQ_RANGES = [5.25]
            for IF_FREQ in IF_FREQ_RANGES:                             
                LO_AMPTD_RANGES = [2]
                for LO_AMPTD in LO_AMPTD_RANGES:
                    #fp = open('/home/pi/Desktop/Golden_1934060020/Tx_Gain_Det/{}, SN#{}, {}C, Ch_{}, {}, {}, {}G, LO_{}dBm, {}.csv'.format(Board_Type, Board_SN, Temperature, Chain_Num, State, Path, IF_FREQ, LO_AMPTD, t),'w')
                    fp = open('/home/pi/Desktop/Data/{}, SN#{}, {}C, Ch_{}, {}, {}, {}G, LO_{}dBm, {}.csv'.format(Board_Type, Board_SN, Temperature, Chain_Num, State, Path, IF_FREQ, LO_AMPTD, t),'w')
                    fpStr = "IF_Freq., Chain_Num, RF_Input, Ch. Freq., Gain, IF_Output_Power, Timestamp \n"   
                    fp.write(fpStr)     
                    fpStr = "(GHz),  , (dBm), (GHz), (dB), (dBm), (Y-M-D H-M-S) \n"      
                    fp.write(fpStr) 
                    SIGGEN_LO.write('POWer ' + str(LO_AMPTD + LO_Path_Loss )+ ' DBM')
                    #sleep(1)
                    
                    
                    RF_FREQ_RANGES = [34.1, 34.3, 34.5, 34.7, 34.9,
                                      35.1, 35.3, 35.5, 35.7, 35.9,
                                      36.1, 36.3, 36.5, 36.7, 36.9,                                     
                                      37.1, 37.3, 37.5, 37.7, 37.9,
                                      38.1, 38.3, 38.5, 38.7, 38.9,
                                      39.1, 39.3, 39.5, 39.7, 39.9,
                                      40.1, 40.3, 40.5, 40.7, 40.9,
                                      41.1, 41.3, 41.5, 41.7, 41.9,
                                      42.1, 42.3, 42.5, 42.7, 42.9,
                                      43.1, 43.3, 43.5, 43.7, 43.9, 44.0]
                    #RF_FREQ_RANGES = [39.5]
                    for RF_FREQ in RF_FREQ_RANGES:
                        FREQ = (RF_FREQ) + float(IF_FREQ)
                        SIGGEN_LO.write('FREQ '+ str(FREQ)+ ' GHz')     # Setting the LO frequency --- even space is critical
                        SIGGEN_1.write('FREQ '+ str(RF_FREQ) + ' GHz')  
                        #IF_INPUT_RANGES = [-37, -33, -29, -25, -21, -17, -13, -9, -5]
                        n = n+1
                        m = m+1
                        print("----------------------------------------------------------- n=", n)
                        #sleep(0.1)
                        if (n==50*len(RF_FREQ_RANGES)):
                            os.remove('dataRxGain.csv')
                            n = 0
                            print("========================================================== dataRxGain.csv file removed")
                            fieldnames = ["RF_Freq", "Gain"]
                            with open('dataRxGain.csv', 'w') as csv_file:
                                csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                                csv_writer.writeheader()
                                
                        if (m==3*len(RF_FREQ_RANGES)):
                            os.remove('dataRxGain1.csv')
                            m = 0
                            print("========================================================== dataRxGain1.csv file removed")
                            fieldnames = ["RF_Freq", "Gain"]
                            with open('dataRxGain1.csv', 'w') as csv_file:
                                csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames1)
                                csv_writer.writeheader()
                                
                        RF_INPUT_RANGES = [-70]    # use -70 dBm for Rx test
                        for RF_INPUT in RF_INPUT_RANGES:
                            AMPTD = RF_INPUT + RF_Input_Path_Loss
                            SIGGEN_1.write('POWer ' + str(AMPTD)+ ' DBM')   
                        

                            #sleep(2)  
                            OFFS = OFFS = IF_Output_Path_Loss                                          
                            SOFFS = str(OFFS)
                            IF_FREQ = str(IF_FREQ)
                            SPECAN.write('SYSTem:DISPlay:UPDate ON')
                            SPECAN.write('DISP:WIND:TRAC:Y:RLEV 0.0') 
                            #SPECAN.write('FREQ:CENT 5.25 GHz') 
                            SPECAN.write('FREQ:CENT '+IF_FREQ+ 'GHz')
                            SPECAN.query('*OPC?') # Using *OPC? query waits until the marker is set
                            #sleep(.2)    
                            SPECAN.write('FREQ:SPAN 1 MHz') 
                            SPECAN.query('*OPC?') 
                            #sleep(.2)                   
                            #SPECAN.write('FREQ:SPAN '+ SSPAN+ 'GHz') 
                            SPECAN.write('BAND 10000Hz') 
                            SPECAN.write('BAND:VID 3000Hz') 
                            SPECAN.write('SWE:POIN 10001') # Setting the sweep points
                            #SPECAN.write('DISP:WIND:TRAC:Y:RLEV:OFFS 0dB')
                            SPECAN.write('DISP:WIND:TRAC:Y:RLEV:OFFS ' +SOFFS+ 'dB')
                            #SPECAN.write('DISP:WIND:TRAC1:MODE AVER')
                            #SPECAN.write('DISP:WIND1:SUBW:TRAC1:MODE AVER')
                            SPECAN.write('INP:ATT 10') # Setting the sweep points -- then set to ATTN 30dB or it will not work
                            SPECAN.write('INIT:CONT On')
                            
                            sleep(0.03)
                            SPECAN.write('CALC1:MARK1:MAX') # Set the marker to the maximum point of the entire trace
                            SPECAN.write('CALC1:MARK1:FUNCtion:CENTer')     
                            #SPECAN.write('CALC1:MARK1:ON') 
                            sleep(.1)
                            
                            markerY1 = float(SPECAN.query('CALC1:MARK1:Y?'))
                            RLEV = markerY1 + 2
                            SRLEV = str(RLEV)
                            SPECAN.write('DISP:WIND:TRAC:Y:RLEV '+SRLEV+ '') 
                            
                            SPECAN.query('*OPC?') 
                            markerX = float(SPECAN.query('CALC1:MARK1:X?'))
                            markerY = float(SPECAN.query('CALC1:MARK1:Y?'))
                            #sleep(1)
     
                            Gain = (markerY - RF_INPUT)
                            
     

                            print ('RF_Input = %0.1f dBm\n' % (RF_INPUT))
                            print ('Chain_Num', Chain_Num)
                            print('RF_Freq. = %0.2fGHz\n' % (RF_FREQ))           
                            
                            IF_OUTPUT_POWER = markerY
                            print ('Output_Power = %0.2fdBm\n' % (IF_OUTPUT_POWER))
                            print('Ch. Freq. = %0.2fGHz, Gain = %0.2fdB\n' % (markerX/1e9, Gain)) 
                            fieldnames = ["RF_Freq", "Gain"]
                          
                            fpStr = str(IF_FREQ) + "," + str(Chain_Num) + "," + str(RF_INPUT) + "," + str(RF_FREQ) + "," + str(round(float(Gain),1)) + "," + str(round(float(IF_OUTPUT_POWER),1))+ "," + str(t) + "," + "\n"
                            fp.write(fpStr) 
                    
                        with open('dataRxGain.csv', 'a') as csv_file:
                            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                            if RF_FREQ == 44.0:
                                info = {"RF_Freq": RF_FREQ, "Gain": float("nan")}
                                csv_writer.writerow(info)
                            else:
                                info = {"RF_Freq": RF_FREQ, "Gain": Gain}
                                csv_writer.writerow(info)
                                
                        with open('dataRxGain1.csv', 'a') as csv_file:
                            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames1)
                            if RF_FREQ == 44.0:
                                info = {"RF_Freq": RF_FREQ, "Gain": float("nan")}
                                csv_writer.writerow(info)
                            else:
                                info = {"RF_Freq": RF_FREQ, "Gain": Gain}
                                #sleep(0.1)
                                csv_writer.writerow(info)                           
                                
                                
                        '''        
                        with open('dataRxGain1.csv', 'w') as csv_file:
                            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames1)
                            csv_writer.writeheader()  
                        '''

                            #sleep(.1)
                        
done                
#subprocess.run('python3.7 ./Rx_fig1_plot.py', shell=True)
fp.close()
ts = time.gmtime()
#SIGGEN_1.write('*RST')    # ------------- Set the Sig-gen to its default state
#SIGGEN_2.write('*RST')    # ------------- Set the Sig-gen to its default state
#SIGGEN_LO.write('*RST')   # ------------- Set the Sig-gen to its default state

Finish = time.strftime("%Y-%m-%d %H:%M:%S", ts)
print("Timestamp Finish = ", Start)
print("Timestamp Finish = ", Finish)






