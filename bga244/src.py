import serial
import time
import yaml

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

class BGA244:
    def __init__(self, port):
        self.port = port
        self.serial = serial.Serial(port, baudrate = BAUDRATE, parity = PARITY, bytesize = BYTESIZE, stopbits = STOPBITS, rtscts = RTSCTS, timeout = TIMEOUT)
        self.__check_connection()
        errors = self.__get_errors()
        print(f"The following error is buffered: {errors}")
        self.config = self.__get_gasconfig()

    def __get_gasconfig(self):
        with open(r"bga244\bga244\gas_config\gases.yaml", "r") as file:
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
    
    def get_gases(self):
        self.serial.write(f"GASP?\r".encode("utf-8"))
        primary = self.serial.readline().decode("utf-8").strip()
        primary = self.__convert_casnr(primary)
        time.sleep(0.1)
        self.serial.write(f"GASS?\r".encode("utf-8"))
        secondary = self.serial.readline().decode("utf-8").strip()
        secondary = self.__convert_casnr(secondary)
        time.sleep(0.1)
        gases = {"prim": primary, "sec": secondary}
        return gases

    def get_binary_gas(self):
        gases = self.get_gases()
        ratos = {f"gas1": [], "gas2": []}
        for i in range(1, 3):
            self.serial.write(f"RATO?{i}\r".encode("utf-8"))
            time.sleep(0.1)
            rato = self.serial.readline().decode("utf-8").strip()
            ratos[f"gas{i}"].append(rato)
            time.sleep(0.1)
        ratos = {f"{gases['prim']}": ratos['gas1'], f"{gases['sec']}": ratos['gas2']}
        return ratos

