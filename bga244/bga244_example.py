import bga244
import time
import sys

#-----------------
# Setup the BGA244
#-----------------
# Connect to the BGA244 via the desired serial code
bga244 = bga244.BGA244("COM3")
# If the config file is not found automatically, give the path to the gases.yaml directly
# bga244 = bga244.BGA244("COM3", "path/to/config/gases.yaml")
# Set mode to Binary Gas Analysis
bga244.set_mode("Binary Gas Analyzer")
# Set concentration type to Mole Fraction
bga244.set_conctype("Mole Fraction")
# Set gas mixture to Argon in Dry Air. This can be done either by gasname or CAS#
bga244.set_gases_binary("7440-37-1", "N2-O2-Ar")
# Get the current units used for measurements
print(bga244.get_units())
#---------------------
# Usage for block heater
#--------------------- 
# Set maximum block heater current drawn
# Set desired temperatur 
# Enable the block heater
# Get status of block heater
bga244.set_bh_currents(0.5) 
bga244.set_bh_temperature(35)
bga244.set_bh_enable(1)
block_heater = bga244.get_block_status() 
print(block_heater)
#-------------------------
# Internal sensor readings
#-------------------------
# Get sensor readings from the BGA244 (Not including the ratio measurement)
ambients = bga244.get_telemetry()
print(ambients)
#--------------
# Miscellaneous
#--------------
# Set the screen to homescreen (if desired)
bga244.set_homescreen()

# Readout of binary gas ratio every 5 sec
while True:
    try:
        # Get the results of the binary gas measurement
        results = bga244.get_binary_ratio()
        for key in results:
            print(f"{key}: {results[key]}")
        # Get the block heater status
        block_heater = bga244.get_block_status()
        print(block_heater)
        # Get sesnsor readings from BGA244
        ambients = bga244.get_telemetry()
        print(ambients)
        time.sleep(5)
    except KeyboardInterrupt:
        # If measurement is stopped manually, disable the heater
        bga244.set_bh_enable(0)
        # Double Check block heater status
        block_heater = bga244.get_block_status()
        print(block_heater)
        sys.exit(0)