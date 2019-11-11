# running today

"""
Created on Sat May 18 18:15:32 2019

@author: wfok

Must run "python Tx_set_EVT2.py off" & "python Tx_set_EVT2.py ch2" or include the script in below.

Should add real-time animation.

"""

import visa
rm = visa.ResourceManager()
rm.list_resources()
#('ASRL1::INSTR', 'ASRL2::INSTR', 'GPIB0::12::INSTR')
SPECAN = rm.open_resource('TCPIP::10.12.116.21::INSTR')
#SPECAN = rm.open_resource('TCPIP::10.12.117.30::INSTR')

#SPECAN = rm.open_resource('TCPIP::10.12.116.65::INSTR')
#print (SPECAN.query('*IDN?')) # Query the Identification string

SIGGEN_1 = rm.open_resource('TCPIP::10.12.118.120::INSTR')
#print(SIGGEN_1.query("*IDN?"))

#SIGGEN_2 = rm.open_resource('TCPIP::10.12.119.122::INSTR')
#print(SIGGEN_2.query("*IDN?"))

SIGGEN_LO = rm.open_resource('TCPIP::10.12.116.5::INSTR')

#print(SIGGEN_LO.query("*IDN?"))

#print(rm.list_resources())


import pyvisa
import numpy as np
import time
import visa
from time import sleep
import csv
import os
import string
#import Tx_set_EVT2


fmt = "%Y-%m-%d %H-%M-%S"
t = time.strftime(fmt)
print("Timestamp Start = ", t)

#import cpld_set

#! /usr/bin/env python

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
import stats_EVT2






# Set the Sig-gens to its default state
#SIGGEN_2.write('*RST')    

# Turn the default Mod On/Off key Off
#SIGGEN_2.write(':OUTPut:MODulation:STATe OFF')        

# Turn the default RF On/Off key On
#SIGGEN_2.write(':OUTPut:STATe ON')                    
 
# Turn-On freq.-ref
#SIGGEN_2.write(':FREQ:REF:STAT ON') 
SPECAN.write_termination = '\n'
SPECAN.write_termination = ''
SPECAN.write('*RST;*CLS') # Reset the instrument, clear the Error queue
SPECAN.write('INIT:CONT OFF') # Switch OFF the continuous sweep
SPECAN.write('SYST:DISP:UPD ON') # Display update ON - switch OFF after debugging
#SPECAN.ext_error_checking() # Error Checking after Initialization 


Board_Type = "4dBm"
Board_SN = "1928060005"
Temperature = "25"    
Chain_Num = "2"
#Polarization = "H"
state = "rx"
#path = "bypass"


fmt = "%Y-%m-%d %H-%M-%S"
#time = datetime.now(timezone('US/Eastern'))
t = time.strftime(fmt)
print("Timestamp Start = ", time.strftime(fmt))


#  10 ft cables system
LO_Path_Loss = 11.5     #11.5               # ---- included 0.3dB WR-22 adapter IL
RF_Path_Loss = 28.5   #40             # ----- incl. 0.25 WR28 adapter loss, able loss 3.5dB, pad loss 30.5dB        
IF_Input_Path_Loss = 9.5      #--- calibrated on 6-11-2019    23dB   



SIGGEN_1.write('*RST')    
SIGGEN_LO.write('*RST')   

SIGGEN_1.write(':OUTPut:MODulation:STATe OFF')                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
SIGGEN_1.write(':OUTPut:STATe ON')                    

SIGGEN_LO.write(':OUTPut:MODulation:STATe OFF')       
SIGGEN_LO.write(':OUTPut:STATe ON')                   

SIGGEN_LO.write(':FREQ:REF:STAT ON') 

# -----------------------------------------------------------


print (SPECAN.query('*IDN?'))
SPECAN.write('*RST;*CLS') 
#SPECAN.write('INIT:CONT OFF') 
SPECAN.write('SYST:DISP:UPD ON') 


Board_Type = input ("Enter Board Type: ")
Board_Type = str(Board_Type)
Board_SN = input ("Enter Board Serial Number: ")
Board_SN = str(Board_SN)   
Temperature = input ("Enter Temperature: ")
Temperature = str(Temperature)    
Chain_Num = input ("Enter Chain Number (make sure to connect the correct RF & IF ports): ")
Chain_Num = str(Chain_Num)
state = input ("Enter tx or rx state: ")

OFFS = RF_Path_Loss
                                                       
SOFFS = str(OFFS)
#IF_FREQ_RANGES = [5.25]
IF_FREQ_RANGES = [5.25]
for IF_FREQ in IF_FREQ_RANGES:                             
    LO_AMPTD_RANGES = [2]
    for LO_AMPTD in LO_AMPTD_RANGES:
        fp = open('/home/pi/Desktop/RF_Det/{}, SN#{}, {}C, Ch{}, {}, {}G, LO_{}dBm, {}.csv'.format(Board_Type, Board_SN, Temperature, Chain_Num, state, IF_FREQ, LO_AMPTD, t),'w')
        #fp = open('/home/pi/Desktop/RF_Detector/LO_Drive_{}dBm, {}.csv'.format(LO_AMPTD, t),'w')
        #fpStr = "Ch. Freq. (GHz), Conversion_Loss (dBm), markerY (dBm), IF_INPUT (dBm), RF_Path_Loss (dB), IF_Path_Loss (dB), Timestamp \n"       
#        fpStr = str(temp.Qorvo_temp_degC) + "," + str(temp.M1_temp_degC) + "," + "\n"
#        fp.write(fpStr) 
        fpStr = "Qor1_Temp (C), Qor2_Temp (C), IF_Freq. (GHz), IF_Input (dBm), Ch. Freq. (GHz), Gain (dB), Ch. Freq. (GHz), Tx_Output_Power (dBm), Ch. Freq. (GHz), V_Det (mV), Timestamp \n"   
        fp.write(fpStr)        
        SIGGEN_LO.write('POWer ' + str(LO_AMPTD + LO_Path_Loss )+ ' DBM')  
        
        IF_INPUT_RANGES = [-30 -20, -16]
        #IF_INPUT_RANGES = [-15]
        for IF_INPUT in IF_INPUT_RANGES:
            AMPTD = IF_Input_Path_Loss + IF_INPUT
            SIGGEN_1.write('POWer ' + str(AMPTD)+ ' DBM')        
        
        
        
            #RF_FREQ_RANGES = [37.1, 37.3, 37.5, 37.7, 37.9, 38.1, 38.3, 38.5, 38.7, 38.9, 39.1, 39.3, 39.5, 39.7, 39.9]
            RF_FREQ_RANGES = [37.1,  37.5,  37.9,  38.3,  38.7,  39.1,  39.5,  39.9]
            for RF_FREQ in RF_FREQ_RANGES:
                SIGGEN_LO.write('FREQ '+ str(RF_FREQ + IF_FREQ)+ ' GHz')     # Setting the LO frequency --- even space is critical
                #SIGGEN_1.write('FREQ '+ str(RF_FREQ)+ ' GHz')  
                SIGGEN_1.write('FREQ '+ str(IF_FREQ) + ' GHz')  
                
        
        
            #IF_INPUT_RANGES = [-40, -38, -36,-34, -32, -30, -28, -26, -24, -22, -20, -18, -16, -14, -12, -10, -8, -6, -4, -2, 0]
            #IF_INPUT_RANGES = [-40, -38]
            #for IF_INPUT in IF_INPUT_RANGES:
                #AMPTD = IF_Input_Path_Loss + IF_INPUT
                #SIGGEN_1.write('POWer ' + str(AMPTD)+ ' DBM')   
            
            #RF_FREQ_RANGES = [37.1, 37.3, 37.5, 37.7, 37.9, 38.1, 38.3, 38.5, 38.7, 38.9, 39.1, 39.3, 39.5, 39.7, 39.9]
            #RF_FREQ_RANGES = [38.5]
            #for RF_FREQ in RF_FREQ_RANGES:
                #SIGGEN.query('FREQuency:MODE CW|FIXed') # Setting the center frequency
                #SIGGEN_LO.write('FREQ '+ str(RF_FREQ + IF_FREQ)+ ' GHz')     # Setting the LO frequency --- even space is critical
                #SIGGEN_1.write('FREQ '+ str(RF_FREQ)+ ' GHz')  
                #SIGGEN_1.write('FREQ '+ str(IF_FREQ) + ' GHz')  
                sleep(.2)  
                OFFS = RF_Path_Loss                                          
                SOFFS = str(OFFS)
                RF_FREQ = str(RF_FREQ)
                SPECAN.write('SYSTem:DISPlay:UPDate ON')
                SPECAN.write('DISP:WIND:TRAC:Y:RLEV 0.0') 
                #SPECAN.write('FREQ:CENT 5.25 GHz') 
                SPECAN.write('FREQ:CENT '+RF_FREQ+ 'GHz')
                SPECAN.query('*OPC?') # Using *OPC? query waits until the marker is set
                sleep(.2)    
                SPECAN.write('FREQ:SPAN 1 MHz') 
                SPECAN.query('*OPC?') 
                sleep(.2)                   
                #SPECAN.write('FREQ:SPAN '+ SSPAN+ 'GHz') 
                SPECAN.write('BAND 10000Hz') 
                SPECAN.write('BAND:VID 1000Hz') 
                SPECAN.write('SWE:POIN 10001') # Setting the sweep points
                #SPECAN.write('DISP:WIND:TRAC:Y:RLEV:OFFS 0dB')
                SPECAN.write('DISP:WIND:TRAC:Y:RLEV:OFFS ' +SOFFS+ 'dB')
                SPECAN.write('INP:ATT 30') # Setting the sweep points -- then set to ATTN 30dB or it will not work
                SPECAN.write('INIT:CONT On')
                sleep(1)
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
                sleep(1)
                #print("M1 ======================= ", 'Marker Frequency %0.1f Hz, Level %0.2f dBm\n' % (markerX, markerY))
                ts = time.gmtime()                             
          
                Gain = (markerY - IF_INPUT)
                #print('Ch. Freq. %0.1f Hz, Gain %0.1f dB\n' % (markerX, Gain))
                
                                        
                
                cpld_adc_set.write(512) #CH0 Power Det Voltage
                cpld_adc_set.write(512) #CH0 Power Det Voltage
                cpld_stats.read(19) #ADC Register
                read_adc = cpld_stats.read(19)
                adc_9bit = read_adc & 0b1111111111
                voltage = (adc_9bit * 2500)/1024
                PWR_DET = voltage
                print ("PWR Det CH0 current =",PWR_DET,"mV")
                
                #cpld_adc_set.write(1536) #CH1 Power Det Voltage      #-------------- cpld.py poke 12 0600
                #cpld_adc_set.write(1536) #CH1 Power Det Voltage
                #cpld_stats.read(19) #ADC Register           # ------------- cpld.py peek 13  3.1.11
                #read_adc = cpld_stats.read(19)
                #adc_9bit = read_adc & 0b1111111111      #------------ delete bits [15:10] and saves bits [9:0]
                #voltage = (adc_9bit * 2500)/1024   #-------------------- conversion
                #PWR_DET = voltage
                #print ("PWR Det CH1 current =",PWR_DET,"mV")
                #print ("IF_INPUT =", IF_INPUT,"dBm")
                
                print ('IF_Input = %0.1f dBm\n' % (IF_INPUT))
                
                #cpld_adc_set.write(2560) #CH2 Power Det Voltage
                #cpld_adc_set.write(2560) #CH2 Power Det Voltage
                #cpld_stats.read(19) #ADC Register
                #read_adc = cpld_stats.read(19)
                #adc_9bit = read_adc & 0b1111111111
                #voltage = (adc_9bit * 2500)/1024
                #PWR_DET = voltage
                #print ("PWR Det CH2 current =",PWR_DET1,"mV")
                
                #cpld_adc_set.write(512) #CH0 Power Det Voltage
                #cpld_adc_set.write(512) #CH0 Power Det Voltage
                
                #cpld_adc_set.write(1536) #CH1 Power Det Voltage      #-------------- cpld.py poke 12 0600
                #cpld_adc_set.write(1536) #CH1 Power Det Voltage
            
                #cpld_adc_set.write(2560) #CH2 Power De
                #cpld_adc_set.write(2560) #CH2 Power Det Voltage
                
                #cpld_adc_set.write(3584) #CH3 Power Det Voltage
                #cpld_adc_set.write(3584) #CH3 Power Det Voltage
                
                #subprocess.run("ssh pi@ipadd " +"cpld_adc_set.write(3584)", shell=True)       
                
                
                
                
                
                cpld_stats.read(19) #ADC Register
                read_adc = cpld_stats.read(19)
                adc_9bit = read_adc & 0b1111111111
                voltage = (adc_9bit * 2500)/1024
                PWR_DET = voltage
                print ('Ch1 Power Detected Voltage = %0.1f mV\n' % (PWR_DET))
                
                OUTPUT_POWER = markerY
                print ('Output_Power = %0.1f dBm\n' % (OUTPUT_POWER))
                print('IF_FREQ = %0.2f GHz, Ch. Freq. = %0.1f GHz, Gain = %0.1f dB\n' % (IF_FREQ, markerX/1000000000, Gain)) 
                '''
                PWR_DET = 0
                if Chain_Num == "0":
                        #PWR_DET = "stats_EVT2.PWR_DET0"
                        print('PWR_DET0 = %0.2fmV, PWR_DET1 = %0.2fmV\n' % ((stats_EVT2.PWR_DET0), stats_EVT2.PWR_DET1)) 
                elif Chain_Num == "1":
                        #PWR_DET = "stats_EVT2.PWR_DET1"
                        print('PWR_DET1 = %0.2fmV, PWR_DET1 = %0.2fmV\n' % ((stats_EVT2.PWR_DET1), stats_EVT2.PWR_DET1)) 
                elif Chain_Num == "2":
                        #PWR_DET = "stats_EVT2.PWR_DET2"
                        print('PWR_DET2 = %0.2fmV, PWR_DET1 = %0.2fmV\n' % ((stats_EVT2.PWR_DET2), stats_EVT2.PWR_DET1)) 
                elif Chain_Num == "3":
                        #PWR_DET = "stats_EVT2.PWR_DET0"
                        print('PWR_DET3 = %0.2fmV, PWR_DET1 = %0.2fmV\n' % ((stats_EVT2.PWR_DET3), stats_EVT2.PWR_DET1)) 
                else: 
                        PWR_DET = 'n/a'
                        '''
                print("CH", Chain_Num)
                print('Qor1_Temp = %0.2f C, Qor2_Temp = %0.2f\n' % (temp.Qorvo_temp_degC, temp.M1_temp_degC)) 
                #print('PWR_DET = %0.2fmV, PWR_DET1 = %0.2fmV\n' % ((stats_EVT2.PWR_DET0), stats_EVT2.PWR_DET1)) 

                #fpStr = str(RF_FREQ) + "," + str(X1) + "," + str(markerY) + "," + str(IF_INPUT) + "," + str(RF_Path_Loss) + "," + str(IF_Input_Path_Loss) + "," + time.strftime(fmt) + "," + "\n"      # ----- similar to writing Excel headings, f.write(fStr) is for writing text, data into excel
                #fpStr = str(RF_FREQ) + "," + str(X1) + "," + str(markerY) + "," + "\n"
                fpStr = str(temp.Qorvo_temp_degC) + "," + str(temp.M1_temp_degC) + "," + str(IF_FREQ) + "," + str(IF_INPUT) + "," + str(RF_FREQ) + "," + str(Gain) + "," + str(RF_FREQ) + "," + str(OUTPUT_POWER) + "," + str(RF_FREQ) + "," + str(PWR_DET) + "," + time.strftime(fmt) + "," + "\n"
                fp.write(fpStr) 

                #sleep(.1)
           

fp.close()
time.strftime(fmt) 
#SIGGEN_1.write('*RST')    # ------------- Set the Sig-gen to its default state
#SIGGEN_2.write('*RST')    # ------------- Set the Sig-gen to its default state
#SIGGEN_LO.write('*RST')   # ------------- Set the Sig-gen to its default state



'''
print("Timestamp Finish = ", time.strftime("%Y-%m-%d %H:%M:%S", ts))

            print ("LO_AMPTD =", LO_AMPTD)
            print ("OFFS =", OFFS)
            #RF_FREQ_RANGES = [37.1]
            for RF_FREQ in RF_FREQ_RANGES:
                #if RF_FREQ >= 38.1 and RF_FREQ <= 39.1:
                if RF_FREQ >= 38.5:
                        LO_AMPTD = 4
                        OFFS = RF_Path_Loss 
                        SIGGEN_LO.write('POWer ' + str(LO_AMPTD + LO_Path_Loss )+ ' DBM')
                        print ("a -- LO_AMPTD =", LO_AMPTD)
                        print ("a -- OFFS =", OFFS)
                else:
                        LO_AMPTD = 0
                        OFFS = RF_Path_Loss 
                        SIGGEN_LO.write('POWer ' + str(LO_AMPTD + LO_Path_Loss )+ ' DBM')
                        print ("b -- OFFS =", OFFS)  
                        
                        print ("b -- LO_AMPTD =", LO_AMPTD)  
                #SIGGEN.query('FREQuency:MODE CW|FIXed') # Setting the center frequency
                LO_FREQ = RF_FREQ + IF_FREQ
                print("LO FREQ =", LO_FREQ)
                
                
'''
