import cpld_set
from Relay_ALC_FSW import alc_fsw
import RFControl
from SA_PhN import SA_PhN 
import lp
import time
import datetime
import os
import numpy as np
import csv
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
import visa

fmt = "%Y-%m-%d %H-%M-%S"
t = time.strftime(fmt)
print("Timestamp Start = ", t)


rm = visa.ResourceManager('@py')
rm.list_resources()
#('ASRL1::INSTR', 'ASRL2::INSTR', 'GPIB0::12::INSTR')
FSW = rm.open_resource('TCPIP::10.12.118.44::INSTR')
print (FSW.query('*IDN?')) # Query the Identification string

SIGGEN_LO = rm.open_resource('TCPIP::10.12.116.61::INSTR')
print(SIGGEN_LO.query("*IDN?"))
print(rm.list_resources())


SIGGEN_LO.write('*RST')   
SIGGEN_LO.write(':OUTPut:MODulation:STATe OFF')       
SIGGEN_LO.write(':OUTPut:STATe ON')                   
SIGGEN_LO.write(':FREQ:REF:STAT ON') 

Board_Type = "EVT4_rev2 Coin"
Board_SN = "1942060002"
Temperature = "25C"    
Path = "0" 
Polarization = " "
state = "Tx"
mode = "EVM"

Qorvo_temp_degC = 0
M1_temp_degC=0

LO_Path_Loss = 1    #  10 ft cable = 12dB loss, direct = 0.5dB loss
RF_Path_Loss = 33.06         #17.5   for Tx and add 30dB or 58.5dB loss for Rx since this siggen could not go down below -20dBm   
IF_Input_Path_Loss = 7.5     # was 8.5 w/o 2-way splitter         


LO_AMPTD = 0
SIGGEN_LO.write('POWer ' + str(LO_AMPTD + LO_Path_Loss )+ ' DBM') 

# IF Parameters

IF_FREQ = 5.25e9
TARGET_POWER = 22
LP_Input = -10 # optimal Litepoint range is -10 ~ -20dBm???
#Level = -15   # -20.5     based on temperature to set attn 
IF_INPUT = LP_Input - IF_Input_Path_Loss 


# Default pre-driver and Qorvo bias 
C_DAC_DEF = 0.2
Q_DAC_12_DEF = 0.3
Q_DAC_3_DEF = 0.3    #  was  0.58
Qorvo_I = 0
CHA3397_I = 0
# Equipment
SA_IP = '10.12.118.44'     # same as FSW thus same IP address
LP_IP = '10.12.115.168'

SA = SA_PhN(SA_IP)
LP = lp.LitePoint(LP_IP,24000)
LP.configure_litepoint('VSG1','frequency',IF_FREQ)
LP.configure_litepoint('VSG1','power', LP_Input)

# Qorvo Bias List
Q_DAC_12_a = np.arange(0.1, 0.2, 0.05)               # -30C test
#Q_DAC_12_a = np.arange(0.0, 0.2,0.1)   
#Q_DAC_12_a = np.arange(0.0,8.12,0.1)
Q_DAC_3_a  = np.arange(0.4, 0.7, 0.1)
#Q_DAC_3_a  = np.arange(0.0, 0.2,0.1)
#Q_DAC_3_a  = np.arange(0.0, 0.55, 0.05)
#Q_DAC_3_a  = np.arange(0.25, 0.75, 0.05)      # -30C test

# Files Setup

now = datetime.datetime.now()
# Name of folder based on date
desco = "{}_{}_{}_{}03/".format(now.month,now.day,now.hour,now.minute)



def GetNewFolder(freq):
    nameDir=desc+'Freq'+str(freq)+'/'
    os.makedirs(os.path.dirname(nameDir),exist_ok=True)

    fileEVM=open(nameDir+'EVM_'+str(freq)+'.csv','w')
    fileC_DAC=open(nameDir+'C_DAC_'+str(freq)+'.csv','w')
    fileOut_Power=open(nameDir+'Out_Power'+str(freq)+'.csv','w')

    fileEVM.write(' ')
    fileC_DAC.write(' ')
    fileOut_Power.write(' ')
    # Write First line
    
    for Bias_3 in Q_DAC_3_a:
        data_line = ",{}".format(Bias_3)
        fileEVM.write(data_line)
        fileC_DAC.write(data_line)
        fileOut_Power.write(data_line)
    
    return [fileEVM,fileC_DAC,fileOut_Power]

    
def EHF_Set(C_DAC_V,Q_DAC_3_V,Q_DAC_12_V, Path):

    RFControl.Set_C_DAC(Path,C_DAC_V)
    RFControl.Set_Q_DAC(Path,3,Q_DAC_3_V)
    RFControl.Set_Q_DAC(Path,12,Q_DAC_12_V)
    

    
def SetPathsOff():
    Paths = [2, 3, 4, 5]
    for Path in Paths:
        RFControl.Set_C_DAC(Path,0)
        RFControl.Set_Q_DAC(Path,3,3.3)
        RFControl.Set_Q_DAC(Path,12,3.3)
        
    print('All paths are off' )
    time.sleep(5)

def SetSA(FREQ):   # need to set to RF
    LP.play_cw2('VSG1')
    SA.set_WLAN()
    SA.set_frequency(FREQ )
    SA.set_SA()
    SA.set_frequency(FREQ)
    time.sleep(1)
    SA.get_peak(1)
    time.sleep(0.5)
    
#fileEVM,fileC_DAC,fileOut_Power]
def GetEVM():
    ## Set FSW to WLAN
    SA.set_WLAN()
    ##Set Lite point to Output 802.11 ac waveform
    LP.play_w2('VSG1')
    time.sleep(1)
    EVM_p = SA.get_EVM()
    print(EVM_p)
    time.sleep(1)
    LP.play_cw2('VSG1')
    time.sleep(0.1)
    SA.set_SA()
    return EVM_p

def save_data(C_DAC,OutputPower,EVM,folders):
    #fileEVM,fileC_DAC,fileOut_Power]
    fileEVM=folders[0]
    fileC_DAC=folders[1]
    fileOut_Power=folders[2]
    EVM = round(EVM,3)
    C_DAC = round(C_DAC,3)
    Output_Power = round(OutputPower,2)
    data_lineEVM = ",{}".format(EVM)
    data_lineC_DAC = ",{}".format(C_DAC)
    data_lineOut_P = ",{}".format(Output_Power)
    fileEVM.write(data_lineEVM)
    fileC_DAC.write(data_lineC_DAC)
    fileOut_Power.write(data_lineOut_P)
    
def SetNextLine(folders,Q_DAC_12):
    fileEVM=folders[0]
    fileC_DAC=folders[1]
    fileOut_Power=folders[2]
    
    data_line = "\n{}".format(Q_DAC_12)
    fileEVM.write(data_line)
    fileC_DAC.write(data_line)
    fileOut_Power.write(data_line)


def CloseFiles(folders):
    fileEVM=folders[0]
    fileC_DAC=folders[1]
    fileOut_Power=folders[2]
    fileEVM.close()
    fileC_DAC.close()
    fileOut_Power.close()
    
 
#fp = open('/home/pi/Desktop/EVT4_1940060001_APCT/Tx_EVM/Board_Type {}, Board_SN#{}, Temperature_{}_C, Chain_{}, State_{}, {}G_IF, LO_Drive_{}dBm, {}.csv'.format(Board_Type, Board_SN, Temperature, Path, state, IF_FREQ, LO_AMPTD, t),'w')
fp = open('/home/pi/Desktop/21dBm_Resistor_Ch0_LP_Input_{}dBm, {}.csv'.format(LP_Input, t),'w')
#fpStr = "Ch. Freq. (GHz), Conversion_Loss (dBm), markerY (dBm), IF_INPUT (dBm), RF_Path_Loss (dB), IF_Path_Loss (dB), Timestamp \n"       
fpStr = "IF_Freq (GHz), Path, Qor1_Temp, Qor2_Temp, Ch. Freq. (GHz), EVM (%), Output_Power (dBm), IF_Input (dBm), Qorvo_I (mA), CHA3398_I (mA), Q_DAC12 (V), Q_DAC3 (V), C_DAC (V), Timestamp \n"     
fp.write(fpStr) 
 
fm = open('/home/pi/Desktop/21dBm_Resistor_EVT4_1942060002_minEVM_Ch0, {}.csv'.format(t),'w')
#fpStr = "Ch. Freq. (GHz), Conversion_Loss (dBm), markerY (dBm), IF_INPUT (dBm), RF_Path_Loss (dB), IF_Path_Loss (dB), Timestamp \n"       
fmStr = "IF_Freq (GHz), Path, Qor1_Temp, Qor2_Temp, Ch. Freq. (GHz), EVM (%), Output_Power (dBm), IF_Input (dBm), Qorvo_I (mA), CHA3398_I (mA), Q_DAC12 (V), Q_DAC3 (V), C_DAC (V), Timestamp \n"     
fm.write(fmStr) 
 
fieldnames = ["Freq", "EVM", "POWER", "tempQ", "tempM", "C_DAC", "Q_DAC_3", "Q_DAC_12", "CHA3398_I", "Qorvo_I"]
#fieldnames = ["Freq", "EVM", "POWER", "C_DAC", "Q_DAC_12"]
#fieldnames = ["Freq", "EVM"]
with open('data_Ch0_EVM.csv', 'w') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    csv_writer.writeheader()


# Set CPLD_RF to Tx manual
cpld_set.write(17,3)


Paths = [2]
FSW.write('MMEM:LOAD:STAT 1, "C:\\R_S\\Instr\\user\\Save_014.dfl"') 


OFFS = RF_Path_Loss                                          
SOFFS = str(OFFS)
FSW.write('DISP:WIND:TRAC:Y:RLEV:OFFS ' +SOFFS+ 'dB')
FSW.write('INP:ATT 0') 
FSW.write('BAND:VID 30000Hz') 


for Path in Paths:
    SetPathsOff()
    desc = desco + 'chan' + str(Path-2)
    EHF_Set(C_DAC_DEF,Q_DAC_3_DEF,Q_DAC_12_DEF,Path)
    
    #for FREQ in [38.1e9]:
    #FREQ_RANGES = [37.1e9, 37.3e9, 39.7e9, 39.9e9] 
    #FREQ_RANGES = np.arange(37.1E9, 40.1E9, 0.2E9)
    FREQ_RANGES = [39.9E9]
    for FREQ in FREQ_RANGES:
        EVM = 100
        minEVM = EVM
        LO_FREQ = FREQ + IF_FREQ
        SIGGEN_LO.write('FREQ '+ str(LO_FREQ)+ ' Hz')
        #with open('dataEVM.csv', 'a') as csv_file:
            #csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
     
        print("READY FOR NEXT...",FREQ)
        
        Folders = GetNewFolder(FREQ)
        
        SetSA(FREQ)
        #SetSynth(FREQ)
        time.sleep(1)
        
        for Q_DAC_12 in Q_DAC_12_a:
            
            SetNextLine(Folders,Q_DAC_12)
            
            for Q_DAC_3 in Q_DAC_3_a:
            
                
                
                if Path == 2:
                        subprocess.run('python ./Tx_set_EVT2.py off', shell=True)
                        subprocess.run('python ./Tx_set_EVT2.py ch0', shell=True)  
                        Qorvo_I = device_I.current("Qorvo_ID_0")
                        CHA3398_I = device_I.current("CHA3398_ID_0")
                            
                elif Path == 3:
                        subprocess.run('python ./Tx_set_EVT2.py off', shell=True)
                        subprocess.run('python ./Tx_set_EVT2.py ch1', shell=True)  
                        Qorvo_I = device_I.current("Qorvo_ID_1")
                        CHA3398_I = device_I.current("CHA3398_ID_1")  
                                   
                elif Path == 4:
                        subprocess.run('python ./Tx_set_EVT2.py off', shell=True)
                        subprocess.run('python ./Tx_set_EVT2.py ch2', shell=True)
                        Qorvo_I = device_I.current("Qorvo_ID_2")
                        CHA3398_I = device_I.current("CHA3398_ID_2")
                elif Path == 5:
                        subprocess.run('python ./Tx_set_EVT2.py off', shell=True)
                        subprocess.run('python ./Tx_set_EVT2.py ch3', shell=True) 
                        Qorvo_I = device_I.current("Qorvo_ID_3")
                        CHA3398_I = device_I.current("CHA3398_ID_3")
                
                else:
                        print("Good Luck!")                                      
 
                
                EHF_Set(C_DAC_DEF,Q_DAC_3,Q_DAC_12,Path)
                FSW.write('DISP:WIND:TRAC:Y:RLEV:OFFS ' +SOFFS+ 'dB')
                FSW.write('BAND:VID 30000Hz') 
                C_DAC, Output_Power = alc_fsw(Path,TARGET_POWER,SA)
                device_I.current("CHA3398_ID_0")
                device_I.current("CHA3398_ID_1")
                device_I.current("CHA3398_ID_2")
                device_I.current("CHA3398_ID_3")
                device_I.current("Qorvo_ID_0")
                device_I.current("Qorvo_ID_1")
                device_I.current("Qorvo_ID_2")
                device_I.current("Qorvo_ID_3")

                
                #C_DAC, Output_Power = alc_fsw(Path,TARGET_POWER,SA)
                time.sleep(1)
                EVM = GetEVM()
                time.sleep(1)
                
                print('EVM= ',EVM)
                print('C_DAC= ',C_DAC)
                print('Q_DAC12= ',Q_DAC_12)
                print('Q_DAC3= ',Q_DAC_3)
                print('Output Power= ',Output_Power)
 
                
                
                save_data(C_DAC,Output_Power, EVM,Folders)
                fpStr = str(IF_FREQ/1e9) + "," + str(Path) + "," + str(tempQor.tempSen(Qorvo_temp_degC)) + "," +  str(tempMac.tempSen(M1_temp_degC)) + "," +  str(FREQ/1e9) + "," + str(EVM) + "," + str(Output_Power) + "," + str(IF_INPUT) + "," + str(Qorvo_I) + "," + str(CHA3398_I) + "," + str(Q_DAC_12) + "," + str(Q_DAC_3) + "," + str(C_DAC) + "," + str(t) + "," + "\n"
                fp.write(fpStr)                 
                tempQ = tempQor.tempSen(Qorvo_temp_degC)
                tempM = tempMac.tempSen(M1_temp_degC)
                
                if minEVM > EVM:
                    minEVM = EVM
                    minOutput_Power = Output_Power
                    minQorvo_I = Qorvo_I
                    minCHA3398_I = CHA3398_I
                    minQ_DAC_12 = Q_DAC_12
                    minQ_DAC_3 = Q_DAC_3 
                    minC_DAC = C_DAC
                    mintempQ = tempQ
                    mintempM = tempM
                    
                    
             
                    
                print("********************************************************* minEVM =", minEVM)
                print("********************************************************* EVM =", EVM)
                #time.sleep(2)
                t = time.strftime(fmt)
            
                #while True:          
                    #info = {"Freq": FREQ/1e9, "EVM": minEVM}
        with open('data_Ch0_EVM.csv', 'a') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            info = {"Freq": FREQ/1e9, "EVM": minEVM, "POWER": minOutput_Power, "tempQ": mintempQ, "tempM": mintempM,
                    "C_DAC": minC_DAC, "Q_DAC_3": minQ_DAC_3, "Q_DAC_12": minQ_DAC_12, "CHA3398_I": CHA3398_I, "Qorvo_I": Qorvo_I}
            csv_writer.writerow(info)
                    
        fmStr = str(IF_FREQ/1e9) + "," + str(Path) + "," + str(mintempQ) + "," +  str(mintempM) + "," +  str(FREQ/1e9) + "," + str(minEVM) + "," + str(minOutput_Power) + "," + str(IF_INPUT) + "," + str(minQorvo_I) + "," + str(minCHA3398_I) + "," + str(minQ_DAC_12) + "," + str(minQ_DAC_3) + "," + str(minC_DAC) + "," + str(t) + "," + "\n"
        fm.write(fmStr)     

        EHF_Set(C_DAC_DEF,Q_DAC_3_DEF,Q_DAC_12_DEF,Path)
    CloseFiles(Folders)
fp.close()
fm.close()

#subprocess.run('python ./Tx_set_EVT2.py off', shell=True)
time.strftime(fmt) 
#SetPathsOff()
    
    
            




