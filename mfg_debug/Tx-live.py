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
import temp_sensor
import tempQor
import tempMac
import device_I
import pyvisa
import numpy as np
import math
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

#print(rm.list_resources())

SPECAN = rm.open_resource('TCPIP::10.12.118.44::INSTR')
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

SIGGEN_1.write('*RST')    
SIGGEN_LO.write('*RST')   
SIGGEN_1.write(':OUTPut:MODulation:STATe OFF')                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
SIGGEN_1.write(':OUTPut:STATe ON')                    
SIGGEN_LO.write(':OUTPut:MODulation:STATe OFF')       
SIGGEN_LO.write(':OUTPut:STATe ON')                   
SIGGEN_LO.write(':FREQ:REF:STAT ON') 

Start = time.strftime(fmt)
print("Timestamp Start = ", Start)

Qorvo_temp_degC = 0
M1_temp_degC=0

LO_Path_Loss = 4    #  10 ft cable = 12dB loss, direct = 0.5dB loss
RF_Path_Loss = 32.5   #24.5         #17.5   for Tx and add 30dB or 58.5dB loss for Rx since this siggen could not go down below -20dBm   
IF_Input_Path_Loss = 8.5
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

Board_Type = "EVT4"
Board_SN =  "1940060001_TTM_Case2"
Temperature = "25C"    
Path = ""
Polarization = " "
State = "Tx"
mode = "gain"

OUTPUT_POWER_37p1 = 0
PWR_DET_37p1 = 0
GAIN_37p1 = 0

OUTPUT_POWER_37p3 = 0
PWR_DET_37p3 = 0
GAIN_37p3 = 0

OUTPUT_POWER_37p5 = 0
PWR_DET_37p5 = 0
GAIN_37p5 = 0

OUTPUT_POWER_37p5 = 0
PWR_DET_37p5 = 0
GAIN_37p5 = 0

OUTPUT_POWER_37p7 = 0
PWR_DET_37p7 = 0
GAIN_37p7 = 0

OUTPUT_POWER_37p9 = 0
PWR_DET_37p9 = 0
GAIN_37p9 = 0


OUTPUT_POWER_38p1 = 0
PWR_DET_38p1 = 0
GAIN_38p1 = 0

OUTPUT_POWER_38p3 = 0
PWR_DET_38p3 = 0
GAIN_38p3 = 0

OUTPUT_POWER_38p5 = 0
PWR_DET_38p5 = 0
GAIN_38p5 = 0

OUTPUT_POWER_38p7 = 0
PWR_DET_38p7 = 0
GAIN_38p7 = 0

OUTPUT_POWER_38p9 = 0
PWR_DET_38p9 = 0
GAIN_38p9 = 0


OUTPUT_POWER_39p1 = 0
PWR_DET_39p1 = 0
GAIN_39p1 = 0

OUTPUT_POWER_39p3 = 0
PWR_DET_39p3 = 0
GAIN_39p3 = 0

OUTPUT_POWER_39p5 = 0
PWR_DET_39p5 = 0
GAIN_39p5 = 0

OUTPUT_POWER_39p7 = 0
PWR_DET_39p7 = 0
GAIN_39p7 = 0

OUTPUT_POWER_39p9 = 0
PWR_DET_39p9 = 0
GAIN_39p9 = 0


#fieldnames = ["RF_FREQ", "OUTPUT_POWER", "PWR_DET"]

fieldnames = ["IF_INPUT",
              "OUTPUT_POWER_37p1", "PWR_DET_37p1", "L_PWR_DET_37p1",
              "OUTPUT_POWER_37p3", "PWR_DET_37p3", "L_PWR_DET_37p3",
              "OUTPUT_POWER_37p5", "PWR_DET_37p5", "L_PWR_DET_37p5",
              "OUTPUT_POWER_37p7", "PWR_DET_37p7", "L_PWR_DET_37p7",
              "OUTPUT_POWER_37p9", "PWR_DET_37p9", "L_PWR_DET_37p9",
              
              "OUTPUT_POWER_38p1", "PWR_DET_38p1", "L_PWR_DET_38p1",
              "OUTPUT_POWER_38p3", "PWR_DET_38p3", "L_PWR_DET_38p3",
              "OUTPUT_POWER_38p5", "PWR_DET_38p5", "L_PWR_DET_38p5",
              "OUTPUT_POWER_38p7", "PWR_DET_38p7", "L_PWR_DET_38p7",
              "OUTPUT_POWER_38p9", "PWR_DET_38p9", "L_PWR_DET_38p9",
              
              "OUTPUT_POWER_39p1", "PWR_DET_39p1", "L_PWR_DET_39p1",
              "OUTPUT_POWER_39p3", "PWR_DET_39p3", "L_PWR_DET_39p3",
              "OUTPUT_POWER_39p5", "PWR_DET_39p5", "L_PWR_DET_39p5",
              "OUTPUT_POWER_39p7", "PWR_DET_39p7", "L_PWR_DET_39p7",
              "OUTPUT_POWER_39p9", "PWR_DET_39p9", "L_PWR_DET_39p9"]


with open('data_V_Det.csv', 'w') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    csv_writer.writeheader()



fieldnames1 = ["IF_INPUT",
              "OUTPUT_POWER_37p1",
              "OUTPUT_POWER_37p3",
              "OUTPUT_POWER_37p5",
              "OUTPUT_POWER_37p7",
              "OUTPUT_POWER_37p9",
              "OUTPUT_POWER_38p1",
              "OUTPUT_POWER_38p3",
              "OUTPUT_POWER_38p5",
              "OUTPUT_POWER_38p7",
              "OUTPUT_POWER_38p9",
              "OUTPUT_POWER_39p1",
              "OUTPUT_POWER_39p3",
              "OUTPUT_POWER_39p5",
              "OUTPUT_POWER_39p7",
              "OUTPUT_POWER_39p9"]


with open('data_P1dB.csv', 'w') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames1)
    csv_writer.writeheader()


IF_INPUT_RANGES = [-37, -33, -29, -25, -21, -17, -13, -9]    # excluded -5 
#IF_INPUT_RANGES = [-37, -25]

for IF_INPUT in IF_INPUT_RANGES:
                    
    fieldnames2 = ["RF_FREQ", "GAIN"]
    filename = "%s.csv" % IF_INPUT
    with open(filename, 'w') as csv_file:
    #with open('data_Gain.csv', 'w') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames2)
        csv_writer.writeheader()        
        




#Chains = [0, 1, 2, 3]
Chains = [0]
for Chain_Num in Chains:

        #IF_FREQ_RANGES = [5.25, 5.57]
        IF_FREQ_RANGES = [5.25]
        for IF_FREQ in IF_FREQ_RANGES:                             
            LO_AMPTD_RANGES = [0]
            for LO_AMPTD in LO_AMPTD_RANGES:
                #EVT4_1940060001_TTM/Tx_Gain_Det
                #fp = open('/home/pi/Desktop/Golden_1934060020/Tx_Gain_Det/{}, SN#{}, {}C, Ch_{}, {}, {}, {}G, LO_{}dBm, {}.csv'.format(Board_Type, Board_SN, Temperature, Chain_Num, State, Path, IF_FREQ, LO_AMPTD, t),'w')
                fp = open('/home/pi/Desktop/{}, SN#{}, {}C, Ch_{}, {}, {}, {}G, LO_{}dBm, {}.csv'.format(Board_Type, Board_SN, Temperature, Chain_Num, State, Path, IF_FREQ, LO_AMPTD, t),'w')
                fpStr = "IF_Freq., Chain_Num, Qor1_Temp, Qor2_Temp, IF_Input, Ch. Freq., Gain, Output_Power, V_Det, C_DAC, Qorvo_I, CHA3398_I, Timestamp \n"   
                fp.write(fpStr)     
                fpStr = "(GHz),  , (C), (C), (dBm), (GHz), (dB), (dBm), (mV), (V), (mA), (mA), (Y-M-D H-M-S) \n"      
                fp.write(fpStr) 
                SIGGEN_LO.write('POWer ' + str(LO_AMPTD + LO_Path_Loss )+ ' DBM')  
                
                IF_INPUT_RANGES = [-37, -33, -29, -25, -21, -17, -13, -9]    # excluded -5 
                #IF_INPUT_RANGES = [-37, -25]

                for IF_INPUT in IF_INPUT_RANGES:

                    AMPTD = IF_Input_Path_Loss + IF_INPUT
                    SIGGEN_1.write('POWer ' + str(AMPTD)+ ' DBM')   
                
                    RF_FREQ_RANGES = [37.1, 37.3, 37.5, 37.7, 37.9, 38.1, 38.3, 38.5, 38.7, 38.9, 39.1, 39.3, 39.5, 39.7, 39.9]
                    #RF_FREQ_RANGES = [37.1, 38.5, 39.9]     
                    for RF_FREQ in RF_FREQ_RANGES:
                        SIGGEN_LO.write('FREQ '+ str(RF_FREQ + IF_FREQ)+ ' GHz')     # Setting the LO frequency --- even space is critical
                        SIGGEN_1.write('FREQ '+ str(IF_FREQ) + ' GHz')  
                        
                                   
                        sleep(.2)  
                        OFFS = OFFS = RF_Path_Loss                                          
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
                        #sleep(.2)                   
                        #SPECAN.write('FREQ:SPAN '+ SSPAN+ 'GHz') 
                        SPECAN.write('BAND 10000Hz') 
                        SPECAN.write('BAND:VID 3000Hz') 
                        SPECAN.write('SWE:POIN 10001') # Setting the sweep points
                        #SPECAN.write('DISP:WIND:TRAC:Y:RLEV:OFFS 0dB')
                        SPECAN.write('DISP:WIND:TRAC:Y:RLEV:OFFS ' +SOFFS+ 'dB')
                        #SPECAN.write('DISP:WIND:TRAC1:MODE AVER')
                        SPECAN.write('DISP:WIND1:SUBW:TRAC1:MODE AVER')
                        SPECAN.write('INP:ATT 10') # Setting the sweep points -- then set to ATTN 30dB or it will not work
                        SPECAN.write('INIT:CONT On')
                        sleep(1)
                        SPECAN.write('CALC1:MARK1:MAX') # Set the marker to the maximum point of the entire trace
                        SPECAN.write('CALC1:MARK1:FUNCtion:CENTer')     
                        #SPECAN.write('CALC1:MARK1:ON') 
                        #sleep(.1)
                        
                        markerY1 = float(SPECAN.query('CALC1:MARK1:Y?'))
                        RLEV = markerY1 + 2
                        SRLEV = str(RLEV)
                        SPECAN.write('DISP:WIND:TRAC:Y:RLEV '+SRLEV+ '') 
                        
                        SPECAN.query('*OPC?') 
                        markerX = float(SPECAN.query('CALC1:MARK1:X?'))
                        markerY = float(SPECAN.query('CALC1:MARK1:Y?'))
                        sleep(1)
 
                        Gain = (markerY - IF_INPUT)

                        C_DAC = 1.5
                        
                        if Chain_Num == 0:
                                subprocess.run('python3.7 ./Tx_set_EVT2.py off', shell=True)
                                subprocess.run('python3.7 ./Tx_set_EVT2.py ch0', shell=True)
                                
                                subprocess.run('python3.7 ./Q_DAC.py write 2 3 0.3', shell=True)
                                subprocess.run('python3.7 ./Q_DAC.py write 2 12 0.3', shell=True)
                                subprocess.run('python3.7 ./C_DAC.py write 2 1.5', shell=True)
                                sleep(0.5)                                           
                                PWR_DET = device_I.Pwr_det("PWR_DET_0")
                                Qorvo_I = device_I.current("Qorvo_ID_0")
                                CHA3398_I = device_I.current("CHA3398_ID_0")
                                
                                                                   
                        elif Chain_Num == 1:
                                subprocess.run('python3.7 ./Tx_set_EVT2.py off', shell=True)
                                subprocess.run('python3.7 ./Tx_set_EVT2.py ch1', shell=True) 
                                subprocess.run('python3.7 ./Q_DAC.py write 3 3 0.3', shell=True)
                                subprocess.run('python3.7 ./Q_DAC.py write 3 12 0.3', shell=True)
                                subprocess.run('python3.7 ./C_DAC.py write 3 1.5', shell=True)
                                                                 
                                PWR_DET = device_I.Pwr_det("PWR_DET_1")    
                                Qorvo_I = device_I.current("Qorvo_ID_1")
                                CHA3398_I = device_I.current("CHA3398_ID_1")  
                                           
                        elif Chain_Num == 2:
                                subprocess.run('python3.7 ./Tx_set_EVT2.py off', shell=True)
                                subprocess.run('python3.7 ./Tx_set_EVT2.py ch2', shell=True)
                                subprocess.run('python3.7 ./Q_DAC.py write 4 3 0.3', shell=True)
                                subprocess.run('python3.7 ./Q_DAC.py write 4 12 0.3', shell=True)
                                subprocess.run('python3.7 ./C_DAC.py write 4 1.5', shell=True) 
                                                                
                                PWR_DET = device_I.Pwr_det("PWR_DET_2") 
                                Qorvo_I = device_I.current("Qorvo_ID_2")
                                CHA3398_I = device_I.current("CHA3398_ID_2")
                                
                        elif Chain_Num == 3:
                                subprocess.run('python3.7 ./Tx_set_EVT2.py off', shell=True)
                                subprocess.run('python3.7 ./Tx_set_EVT2.py ch3', shell=True)
                                subprocess.run('python3.7 ./Q_DAC.py write 5 3 0.3', shell=True)
                                subprocess.run('python3.7 ./Q_DAC.py write 5 12 0.3', shell=True)
                                subprocess.run('python3.7 ./C_DAC.py write 5 1.5', shell=True)                       
                                
                                PWR_DET = device_I.Pwr_det("PWR_DET_3")  
                                Qorvo_I = device_I.current("Qorvo_ID_3")
                                CHA3398_I = device_I.current("CHA3398_ID_3")
                        else:
                                print("Good Luck!")       
                        
                        #subprocess.run('python3 ./Tx_set_EVT2.py off', shell=True)

                        print ('IF_Input = %0.1f dBm\n' % (IF_INPUT))
                        print ('Chain_Num', Chain_Num)
                        #print ('Power Detected Voltage = %0.2fmV\n' % (PWR_DET))
                        print('IF_Freq. = %0.2fGHz\n' % (IF_FREQ))           
                        
                        OUTPUT_POWER = markerY
                        print ('Output_Power = %0.2fdBm\n' % (OUTPUT_POWER))
                        print('Ch. Freq. = %0.2fGHz, Gain = %0.2fdB\n' % (markerX/1e9, Gain)) 
                        
                        fpStr = str(IF_FREQ) + "," + str(Chain_Num) + "," + str(round(float(tempQor.tempSen(Qorvo_temp_degC)), 1)) + "," +  str(round(float(tempMac.tempSen(M1_temp_degC)), 1)) + "," +  str(IF_INPUT) + "," + str(RF_FREQ) + "," + str(round(float(Gain),1)) + "," + str(round(float(OUTPUT_POWER),1))+ "," + str(round(PWR_DET, 2)) + "," + str(round(float(C_DAC), 1)) + "," + str(round(float(Qorvo_I), 1)) + "," + str(round(float(CHA3398_I), 1)) + "," + str(t) + "," + "\n"
                        fp.write(fpStr) 

                        
                        print ("Power_det", PWR_DET)
                        
                        
                        filename = "%s.csv" % IF_INPUT
                        with open(filename, 'a') as csv_file:
                        #with open('data_Gain.csv', 'a') as csv_file:   
                            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames2)
                            info = {"RF_FREQ": RF_FREQ, "GAIN": Gain}
                            csv_writer.writerow(info)
                        #sleep(3)
                        if RF_FREQ == '37.1':
                            OUTPUT_POWER_37p1 = OUTPUT_POWER
                            PWR_DET_37p1 = PWR_DET
                            GAIN_37p1 = Gain
                            
                            
                        elif RF_FREQ == '37.3':
                            OUTPUT_POWER_37p3 = OUTPUT_POWER
                            PWR_DET_37p3 = PWR_DET
                            #GAIN_37p3 = Gain
                            
                            
                            print ("++++++++++++++++++++++++++++++++++++++++++++++++++ RF_FREQ", RF_FREQ)
                        elif RF_FREQ == '37.5':
                            OUTPUT_POWER_37p5 = OUTPUT_POWER
                            PWR_DET_37p5 = PWR_DET
                            #GAIN_37p5 = Gain                          
                            
                            
                        elif RF_FREQ == '37.7':
                            OUTPUT_POWER_37p7 = OUTPUT_POWER
                            PWR_DET_37p7 = PWR_DET
                            #GAIN_37p7 = Gain
                            
                            
                        elif RF_FREQ == '37.9':
                            OUTPUT_POWER_37p9 = OUTPUT_POWER
                            PWR_DET_37p9 = PWR_DET
                            #GAIN_37p9 = Gain                       
                            
                            
                        elif RF_FREQ == '38.1':
                            OUTPUT_POWER_38p1 = OUTPUT_POWER
                            PWR_DET_38p1 = PWR_DET
                            #GAIN_38p1 = Gain
                            
                            
                        elif RF_FREQ == '38.3':
                            OUTPUT_POWER_38p3 = OUTPUT_POWER
                            PWR_DET_38p3 = PWR_DET
                            #GAIN_38p3 = Gain                         
                            
                            
                        elif RF_FREQ == '38.5':
                            OUTPUT_POWER_38p5 = OUTPUT_POWER
                            PWR_DET_38p5 = PWR_DET
                            #GAIN_38p5 = Gain
                            
                            
                        elif RF_FREQ == '38.7':
                            OUTPUT_POWER_38p7 = OUTPUT_POWER
                            PWR_DET_38p7 = PWR_DET
                            #GAIN_38p7 = Gain                         
                            
                            
                        elif RF_FREQ == '38.9':
                            OUTPUT_POWER_38p9 = OUTPUT_POWER
                            PWR_DET_38p9 = PWR_DET
                            #GAIN_38p9 = Gain                        
                            
                            
                        elif RF_FREQ == '39.1':
                            OUTPUT_POWER_39p1 = OUTPUT_POWER
                            PWR_DET_39p1 = PWR_DET
                            #GAIN_39p1 = Gain
                            
                            
                        elif RF_FREQ == '39.3':
                            OUTPUT_POWER_39p3 = OUTPUT_POWER
                            PWR_DET_39p3 = PWR_DET
                            #GAIN_39p3 = Gain
                           
                        
                        elif RF_FREQ == '39.5':
                            OUTPUT_POWER_39p5 = OUTPUT_POWER
                            PWR_DET_39p5 = PWR_DET
                            #GAIN_39p5 = Gain                       
                           
                            
                        elif RF_FREQ == '39.7':
                            OUTPUT_POWER_39p7 = OUTPUT_POWER
                            PWR_DET_39p7 = PWR_DET
                            #GAIN_39p7 = Gain 
                           
                            
                        elif RF_FREQ == '39.9':
                            OUTPUT_POWER_39p9 = OUTPUT_POWER
                            PWR_DET_39p9 = PWR_DET
                            #GAIN_39p9 = Gain                  
                           
                        else:
                            print("Good Luck")
                        

                            
                    with open('data_V_Det.csv', 'a') as csv_file:
                        print ("========================================================== RF_FREQ", RF_FREQ)
                        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                        info = {"IF_INPUT": IF_INPUT,
                                "OUTPUT_POWER_37p1": OUTPUT_POWER_37p1, "PWR_DET_37p1": PWR_DET_37p1, "L_PWR_DET_37p1": 10*math.log(PWR_DET_37p1, 10),
                                "OUTPUT_POWER_37p3": OUTPUT_POWER_37p3, "PWR_DET_37p3": PWR_DET_37p3, "L_PWR_DET_37p3": 10*math.log(PWR_DET_37p3, 10),
                                "OUTPUT_POWER_37p5": OUTPUT_POWER_37p5, "PWR_DET_37p5": PWR_DET_37p5, "L_PWR_DET_37p5": 10*math.log(PWR_DET_37p5, 10),
                                "OUTPUT_POWER_37p7": OUTPUT_POWER_37p7, "PWR_DET_37p7": PWR_DET_37p7, "L_PWR_DET_37p7": 10*math.log(PWR_DET_37p7, 10),
                                "OUTPUT_POWER_37p9": OUTPUT_POWER_37p9, "PWR_DET_37p9": PWR_DET_37p9, "L_PWR_DET_37p9": 10*math.log(PWR_DET_37p9, 10),
                                
                                "OUTPUT_POWER_38p1": OUTPUT_POWER_38p1, "PWR_DET_38p1": PWR_DET_38p1, "L_PWR_DET_38p1": 10*math.log(PWR_DET_38p1, 10),
                                "OUTPUT_POWER_38p3": OUTPUT_POWER_38p3, "PWR_DET_38p3": PWR_DET_38p3, "L_PWR_DET_38p3": 10*math.log(PWR_DET_38p3, 10),
                                "OUTPUT_POWER_38p5": OUTPUT_POWER_38p5, "PWR_DET_38p5": PWR_DET_38p5, "L_PWR_DET_38p5": 10*math.log(PWR_DET_38p5, 10),
                                "OUTPUT_POWER_38p7": OUTPUT_POWER_38p7, "PWR_DET_38p7": PWR_DET_38p7, "L_PWR_DET_38p7": 10*math.log(PWR_DET_38p7, 10),
                                "OUTPUT_POWER_38p9": OUTPUT_POWER_38p9, "PWR_DET_38p9": PWR_DET_38p9, "L_PWR_DET_38p9": 10*math.log(PWR_DET_38p9, 10),
                                
                                "OUTPUT_POWER_39p1": OUTPUT_POWER_39p1, "PWR_DET_39p1": PWR_DET_39p1, "L_PWR_DET_39p1": 10*math.log(PWR_DET_39p1, 10),
                                "OUTPUT_POWER_39p3": OUTPUT_POWER_39p3, "PWR_DET_39p3": PWR_DET_39p3, "L_PWR_DET_39p3": 10*math.log(PWR_DET_39p3, 10),
                                "OUTPUT_POWER_39p5": OUTPUT_POWER_39p5, "PWR_DET_39p5": PWR_DET_39p5, "L_PWR_DET_39p5": 10*math.log(PWR_DET_39p5, 10),
                                "OUTPUT_POWER_39p7": OUTPUT_POWER_39p7, "PWR_DET_39p9": PWR_DET_39p7, "L_PWR_DET_39p7": 10*math.log(PWR_DET_39p7, 10),
                                "OUTPUT_POWER_39p9": OUTPUT_POWER_39p9, "PWR_DET_39p9": PWR_DET_39p9, "L_PWR_DET_39p9": 10*math.log(PWR_DET_39p9, 10)}
                                
                        csv_writer.writerow(info)
                        
                    with open('data_P1dB.csv', 'a') as csv_file:
                        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames1)
                        info = {"IF_INPUT": IF_INPUT,
                                "OUTPUT_POWER_37p1": OUTPUT_POWER_37p1,
                                "OUTPUT_POWER_37p3": OUTPUT_POWER_37p3,
                                "OUTPUT_POWER_37p5": OUTPUT_POWER_37p5,
                                "OUTPUT_POWER_37p7": OUTPUT_POWER_37p7,
                                "OUTPUT_POWER_37p9": OUTPUT_POWER_37p9,
                                
                                "OUTPUT_POWER_38p1": OUTPUT_POWER_38p1,
                                "OUTPUT_POWER_38p3": OUTPUT_POWER_38p3,
                                "OUTPUT_POWER_38p5": OUTPUT_POWER_38p5,
                                "OUTPUT_POWER_38p7": OUTPUT_POWER_38p7,
                                "OUTPUT_POWER_38p9": OUTPUT_POWER_38p9,
                                
                                "OUTPUT_POWER_39p1": OUTPUT_POWER_39p1,
                                "OUTPUT_POWER_39p3": OUTPUT_POWER_39p3,
                                "OUTPUT_POWER_39p5": OUTPUT_POWER_39p5,
                                "OUTPUT_POWER_39p7": OUTPUT_POWER_39p7,
                                "OUTPUT_POWER_39p9": OUTPUT_POWER_39p9}
                        csv_writer.writerow(info)
                        
  
                        
#subprocess.run('python3 ./Tx_set_EVT2.py off', shell=True)
fp.close()
ts = time.gmtime()
#SIGGEN_1.write('*RST')    # ------------- Set the Sig-gen to its default state
#SIGGEN_2.write('*RST')    # ------------- Set the Sig-gen to its default state
#SIGGEN_LO.write('*RST')   # ------------- Set the Sig-gen to its default state

Finish = time.strftime("%Y-%m-%d %H:%M:%S", ts)
print("Timestamp Finish = ", Start)
print("Timestamp Finish = ", Finish)





