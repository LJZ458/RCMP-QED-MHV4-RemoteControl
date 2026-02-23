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

log("Turning all channels ON\n")
for ch in channels:
    MHV4_1.set_on(ch)

time.sleep(3)

# ---------- RAMP UP ----------
log("Ramping up voltage...\n")

for step in range(11):
    v = preset_Volt * step / 10

    for ch in channels:
        MHV4_1.set_voltage(ch, v)
        cur1 = MHV4_1.get_current(ch)

        if abs(cur1) > 2.5:
            print("CURRENT LIMIT REACHED — SHUTTING DOWN ALL CHANNELS!")

            # Ramp down safely
            for ch_shutdown in channels:
                MHV4_1.set_voltage(ch_shutdown, 0)
                time.sleep(1)

            time.sleep(300)

            for ch_shutdown in channels:
                MHV4_1.set_off(ch_shutdown)

            exit()

    log(f"Ramped to {v:.1f} V")
    time.sleep(10)
sys.exit(0)
