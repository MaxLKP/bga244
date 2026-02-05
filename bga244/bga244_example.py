import bga244
import time

# Setup the BGA244
bga244 = bga244.BGA244("COM3")
bga244.set_mode("Binary Gas Analyzer")
bga244.set_conctype("Mole Fraction")
bga244.set_gases_binary("CO2", "N2-O2-Ar")

# Readout of binary gas ratio every 5 sec
while True:
    result = bga244.get_binary_ratio()
    print(result)
    time.sleep(5)
