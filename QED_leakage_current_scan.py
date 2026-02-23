#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import mhv4lib
import time
import numpy as np

def log(text):
    print(text)

##### check USB connection and verify port connect USBA cable 1 by 1 to check #####
MHV4_1 = mhv4lib.MHV4('/dev/ttyUSB0', baud=9600)
MHV4_2 = mhv4lib.MHV4('/dev/ttyUSB1', baud=9600)

##### MHV4_1 bias QED2,4,6     MHV4_2 bias QED1,3,5 #####

scan_voltages = np.arange(0.5, 200.5, 0.5)  # 0.5 V to 200 V in 0.5 V steps
channels = [0, 1, 2]

# Create separate result arrays for each power supply
res1 = np.zeros((len(scan_voltages), len(channels) + 1))
res2 = np.zeros((len(scan_voltages), len(channels) + 1))

# initialize first column with voltages
for i, volt in enumerate(scan_voltages):
    res1[i][0] = volt
    res2[i][0] = volt

# ---------- START SCANNING ----------
log("\nPreparing to start the scan...\n")

# Safety: set all channels to OFF and 0 V
log("Setting all voltages to zero...\n")
for ch in channels:
    MHV4_1.set_off(ch)
    MHV4_1.set_voltage(ch, 0)
    MHV4_2.set_off(ch)
    MHV4_2.set_voltage(ch, 0)

time.sleep(3)

log("Turning all channels ON...\n")
for ch in channels:
    MHV4_1.set_on(ch)
    MHV4_2.set_on(ch)

time.sleep(3)

log("Start scanning voltages...\n")

for i, volt in enumerate(scan_voltages):

    log(f"Scanning voltage: {volt:.2f} V")

    # set voltage on all channels
    for ch in channels:
        MHV4_1.set_voltage(ch, volt)
        MHV4_2.set_voltage(ch, volt)

    time.sleep(10)   # wait for ramp-up

    # read currents
    for ch in channels:
        cur1 = MHV4_1.get_current(ch)
        cur2 = MHV4_2.get_current(ch)

        res1[i][ch + 1] = cur1
        res2[i][ch + 1] = cur2

        if cur1 > 2.5 or cur2 > 2.5:
            print("CURRENT LIMIT REACHED! STOPPING !!!!")
            MHV4_1.close()
            MHV4_2.close()
            exit()

# ---------- RAMP DOWN SAFELY ----------
log("\nStopping scan... ramping voltages to zero...\n")

for ch in channels:
    curvoltage = MHV4_1.get_voltage(ch)
    curvoltage2 = MHV4_2.get_voltage(ch)
    print(f"ch {ch} current voltage {curvoltage}")

    while abs(curvoltage) > 0:
        MHV4_1.set_voltage(ch, int(abs(curvoltage)) - 1)
        time.sleep(5)
        curvoltage = MHV4_1.get_voltage(ch)
    while abs(curvoltage2) > 0:
        MHV4_2.set_voltage(ch, int(abs(curvoltage2)) - 1)
        time.sleep(5)
        curvoltage2 = MHV4_2.get_voltage(ch)

    MHV4_1.set_off(ch)
    MHV4_2.set_off(ch)

MHV4_1.close()
MHV4_2.close()

# ---------- WRITE OUTPUT FILES (NO np.savetxt) ----------
with open("output_MHV4_1.txt", "w") as f1:
    for row in res1:
        line = " ".join(f"{x:.3f}" for x in row)
        f1.write(line + "\n")

with open("output_MHV4_2.txt", "w") as f2:
    for row in res2:
        line = " ".join(f"{x:.3f}" for x in row)
        f2.write(line + "\n")

print("\nScan finished.")
print("Saved files:")
print("output_MHV4_1.txt")
print("output_MHV4_2.txt")
