#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Leakage current monitor for BB7 DSSSD — writes to file every 5 minutes
# This is a test version for utility development
import sys
import mhv4lib
import time
from datetime import datetime

preset_Volt = 170
channels = [1]
SLEEP_TIME = 300

def log(text):
    print(text)

# --- Connect to supply ---
MHV4_1 = mhv4lib.MHV4('/dev/ttyUSB0', baud=9600)
# MHV4_2 = mhv4lib.MHV4('/dev/ttyUSB1', baud=9600)
s
# ---------- SAFETY: ZERO VOLTAGE ----------
log("\nSetting all voltages to zero...\n")
for ch in channels:
    MHV4_1.set_off(ch)
    MHV4_1.set_voltage(ch, 0)

time.sleep(3)
log("Turning all channels OFF\n")

sys.exit(0)
