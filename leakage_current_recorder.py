#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Script to record leakage current for BB7 DSSSD
import mhv4lib
import time
import numpy as np
from datetime import datetime

#record 96 events per file with each data point collected evert 5 min total of 8hrs 
t_dur = 96
def log(text):
	print(text)
#####check USB connection and verify port. Need to chmod 666 to allow read and write
mymhv4 = mhv4lib.MHV4('/dev/ttyUSB0', baud=9600)
preset_Volt = 170


channels = [0]
#####create a 2d array with col1 voltage, col2... for leakage currents of channel2.....
leak = np.zeros( ( t_dur, (len(channels)+1) ) )

##initialize 2d array with col1 of time col2....... of leakage currents


# START
log('Preparing to start ...\n')

# Set all channels to OFF and zero voltage
log('Setting voltages to zero\n')
for ch in channels:
	mymhv4.set_off(ch)
	mymhv4.set_voltage(ch, 0)

log('Voltages set to zero. Turning all channels ON\n')
time.sleep(3)
for ch in channels:
	mymhv4.set_on(ch)

log('Channels turned ON.\n')
time.sleep(3)

log('Start voltages Ramping.\n')
i=0
for ch in channels:
	while i<=10:
	
		mymhv4.set_voltage(ch, preset_Volt*i/10)
		cur = mymhv4.get_current(ch)
		if cur > 2.5:  # ramping safety check
			## for BB7 1mm thick DSSSD the leakage current will ramp above 1uA but shouldn't be higher than 2.5 
			print("CURRENT LIMIT REACHED! STOPPING !!!!")
			exit()


i=0
while true:
	current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
	while i<=t_dur:
		for ch in channels:
			cur = mymhv4.get_current(ch)
			leak[i][ch+1] = mymhv4.get_current(ch)
			leak[i][0] = datetime.now()
			if cur > 2.5:  # operation safety check
			## for BB7 1mm thick DSSSD the leakage current will ramp above 1uA but shouldn't be higher than 2.5 
			print("CURRENT LIMIT REACHED! STOPPING !!!!")
				exit()
			i = i+1
			time.sleep(300)
	
	output_str = current_datetime + ".txt"
	np.savetxt(output_str, leak, fmt='%.3f', delimiter=' ')
	i=0
		
		







