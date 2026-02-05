import serial
import time
import yaml
import os

# https://github.com/MaxLKP/bga244?tab=readme-ov-file#readme

# Manual:
# https://www.thinksrs.com/downloads/pdfs/manuals/BGA244m.pdf
# Fabric Settings Gases
# https://www.thinksrs.com/downloads/pdfs/applicationnotes/BGA244%20Gas%20Table.pdf

# Serial Config
BAUDRATE = 9600
PARITY = "N"
BYTESIZE = 8
STOPBITS = 1
RTSCTS = 1
TIMEOUT = 5

MODES = {"Binary Gas Analyzer": 1, "Gas Purity Analyzer": 2, "Physical Measurements": 3}
CONCTYPES = {"Mole Fraction": 1, "Mass Fraction": 2}

class BGA244:
    def __init__(self, port):
        self.port = port
        self.serial = serial.Serial(port, baudrate = BAUDRATE, parity = PARITY, bytesize = BYTESIZE, stopbits = STOPBITS, rtscts = RTSCTS, timeout = TIMEOUT)
        self.__check_connection()
        errors = self.__get_errors()
        print(f"The following error is buffered: {errors}")
        self.config = self.__get_gasconfig()

    def __get_gasconfig(self):
        with open(os.path.join("bga244", "bga244", "gas_config", "gases.yaml")) as file:
            config = yaml.safe_load(file)
        return config
    
    def __convert_casnr(self, casnr): # Takes CAS#, returns Gasname 
        return self.config["cas#"][casnr]

    def __convert_gas(self, gasname): # Takes Gasname, returns CAS#
        return self.config["gas"][gasname]

    def __check_connection(self):
        if self.serial:
            print(f"Connected to BGA244 on Port {self.port}")
        else: 
            print("Could not connect to BGA244")

    def __get_errors(self):
        self.serial.write(b"LERR?\r")
        time.sleep(0.1)
        error = self.serial.readline().decode("utf-8").strip()
        if error:
            return error
        else:
            return 0
    
    def __gas_check(self, gas1, gas2):
        gases_out = self.get_gases()
        gases_in = {"prim": gas1, "sec": gas2}
        checksum = 0
        for key in gases_in:
            if gases_out[key] == gases_in[key]:
                checksum += 1
            else: pass
        if checksum == 2:
            print(f"Gases set to {gas1} and {gas2} success.")
        else:
            print("Gases not set correctly.")

    def __get_uncertainties(self):
        self.serial.write(f"UNCT?\r".encode("utf-8"))
        time.sleep(0.1)
        uncertainty = self.serial.readline().decode("utf-8").strip()
        time.sleep(0.1)
        return uncertainty

    def set_conctype(self, conctype):
        conctypeint = CONCTYPES[conctype]
        self.serial.write(f"BCTP {conctypeint}\r".encode("utf-8"))
        time.sleep(0.1)
        conctype_read = self.get_conctype()
        if int(conctype_read) == int(conctypeint):
            print(f"Binary Concentration Type set to {conctype} success.")
        else:
            print("Error while setting Binary Concentration Type")
    
    def get_conctype(self):
        self.serial.write(f"BCTP?\r".encode("utf-8"))
        time.sleep(0.1)
        conctype = self.serial.readline().decode("utf-8").strip()
        time.sleep(0.1)
        return conctype

    def get_gases(self):
        self.serial.write(f"GASP?\r".encode("utf-8"))
        time.sleep(0.1)
        primary = self.serial.readline().decode("utf-8").strip()
        time.sleep(0.1)
        primary = self.__convert_casnr(primary)
        self.serial.write(f"GASS?\r".encode("utf-8"))
        time.sleep(0.1)
        secondary = self.serial.readline().decode("utf-8").strip()
        time.sleep(0.1)
        secondary = self.__convert_casnr(secondary)
        gases = {"prim": primary, "sec": secondary}
        return gases
    
    def set_gas_singular(self, gas):
        if gas in self.config["gas"].keys():
            gas_conv = self.__convert_gas(gas)
        elif gas in self.config["cas#"].keys():
            gas_conv = gas
        else:
            print(f"Gas {gas} not found in config.")
        self.serial.write(f"GASP {gas_conv}\r".encode("utf-8"))

    def set_gases_binary(self, gas1, gas2):
        gases = [gas1, gas2]
        gases_conv = []
        for gas in gases:
            if gas in self.config["gas"].keys():
                gases_conv.append(self.__convert_gas(gas))
            elif gas in self.config["cas#"].keys():
                gases_conv.append(gas)
            else: 
                print(f"Gas {gas} not found in config.")
        self.serial.write(f"GASP {gases_conv[0]}\r".encode("utf-8"))
        time.sleep(0.1)
        self.serial.write(f"GASS {gases_conv[1]}\r".encode("utf-8"))
        time.sleep(0.1)
        self.__gas_check(gas1, gas2)

    def get_binary_ratio(self):
        gases = self.get_gases()
        ratos = {f"gas1": [], "gas2": []}
        for i in range(1, 3):
            self.serial.write(f"RATO?{i}\r".encode("utf-8"))
            time.sleep(0.1)
            rato = self.serial.readline().decode("utf-8").strip()
            ratos[f"gas{i}"].append(rato)
            time.sleep(0.1)
        uncertainty = self.__get_uncertainties()
        ratos = {f"{gases['prim']}": float(ratos['gas1'][0]), f"{gases['sec']}": float(ratos['gas2'][0]), "uncert": uncertainty}
        return ratos
    
    def set_mode(self, mode):
        if MODES[mode]:
            pass
        else: print(f"Unrecognized Mode {mode}.")
        modeint = MODES[mode]
        self.serial.write(f"MSMD{modeint}\r".encode("utf-8"))
        time.sleep(0.1)
        

        


