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

    # Write command to BGA244
    def __write_command(self, command: str) -> None:
        command = command + "\r"
        command = command.encode("utf-8") 
        self.serial.write(command)
        time.sleep(0.1)

    # Read BGA Response to command
    def __read_response(self):
        response = self.serial.readline().decode("utf-8").strip()
        time.sleep(0.1)
        return response

    # Get list of gases from config file
    def __get_gasconfig(self):
        with open(os.path.join("bga244", "bga244", "gas_config", "gases.yaml")) as file:
            config = yaml.safe_load(file)
        return config
    
    # Take CAS#, return Gasname
    def __convert_casnr(self, casnr):  
        return self.config["cas#"][casnr]

    # Take Gasname, return CAS#
    def __convert_gas(self, gasname): 
        return self.config["gas"][gasname]

    # Check for succesfull serial connection
    def __check_connection(self) -> None:
        if self.serial.isOpen():
            print(f"Connected to BGA244 on Port {self.port}")
        else: 
            print("Could not connect to BGA244")

    # Read Errorbuffer
    def __get_errors(self):
        self.__write_command("LERR?")
        self.error = self.__read_response()
        if self.error:
            return self.error
        else:
            return 0
    
    # Check if gases were set correctly
    def __gas_check(self, gas1, gas2) -> None: 
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

    # Get uncertainties of Measurement
    def __get_uncertainties(self): 
        self.__write_command("UNCT?")
        uncertainty = self.__read_response()
        return uncertainty

    # Set unit for ratio measurement
    def set_conctype(self, conctype) -> None: 
        conctypeint = CONCTYPES[conctype]
        self.__write_command(f"BCTP {conctypeint}")
        conctype_read = self.get_conctype()
        if int(conctype_read) == int(conctypeint):
            print(f"Binary Concentration Type set to {conctype} success.")
        else:
            print("Error while setting Binary Concentration Type")
    
    # Get unit of ratio measurement
    def get_conctype(self):
        self.__write_command("BCTP?")
        conctype = self.__read_response()
        return conctype

    # Get currently set gases
    def get_gases(self):
        self.__write_command("GASP?")
        primary = self.__read_response()
        primary = self.__convert_casnr(primary)
        self.__write_command("GASS?")
        secondary = self.__read_response()
        secondary = self.__convert_casnr(secondary)
        gases = {"prim": primary, "sec": secondary}
        return gases
    
    # Set gas for purity analyisis
    def set_gas_singular(self, gas) -> None:
        if gas in self.config["gas"].keys():
            gas_conv = self.__convert_gas(gas)
        elif gas in self.config["cas#"].keys():
            gas_conv = gas
        else:
            print(f"Gas {gas} not found in config.")
        self.__write_command(f"GASP {gas_conv}")

    # Set gases for binary gas analysis
    def set_gases_binary(self, gas1, gas2) -> None:
        gases = [gas1, gas2]
        gases_conv = []
        for gas in gases:
            if gas in self.config["gas"].keys():
                gases_conv.append(self.__convert_gas(gas))
            elif gas in self.config["cas#"].keys():
                gases_conv.append(gas)
            else: 
                print(f"Gas {gas} not found in config.")
        self.__write_command(f"GASP {gases_conv[0]}")
        self.__write_command(f"GASS {gases_conv[1]}")
        self.__gas_check(gas1, gas2)

    # Get result of binary gas analysis
    def get_binary_ratio(self):
        gases = self.get_gases()
        ratos = {f"gas1": [], "gas2": []}
        for i in range(1, 3):
            self.__write_command(f"RATO?{i}%")
            rato = self.__read_response()
            ratos[f"gas{i}"].append(rato)
        uncertainty = self.__get_uncertainties()
        ratos = {f"{gases['prim']}": float(ratos['gas1'][0]), f"{gases['sec']}": float(ratos['gas2'][0]), "uncert": uncertainty}
        return ratos
    
    # Set measurement mode
    def set_mode(self, mode) -> None:
        if MODES[mode]:
            pass
        else: print(f"Unrecognized Mode {mode}.")
        modeint = MODES[mode]
        self.__write_command(f"MSMD {modeint}")

    # Set Relative Mode - To be tested
    def set_relmode(self):
        self.__write_command("RELH")

    # Get readings of internal sensor
    def get_telemetry(self):
        self.__write_command("PRAM? bar")
        pressure_amb = self.__read_response()
        pressure_gas = self.__write_command("PRES? bar")
        pressure_gas = self.__read_response()
        self.__write_command("TCEL? C")
        temperature_cell = self.__read_response()
        #self.__write_command("XALL?")
        #xall = self.__read_response()
        values = {"P_amb": pressure_amb, "P_gas": pressure_gas, "T_cell": temperature_cell}
        return values


    
        

        


