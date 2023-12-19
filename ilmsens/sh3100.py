import os
from ctypes import cdll

class MEXPLORE_SH3100():

    LIB_PATH = os.path.join("usr", "lib", "libilmsens_hal.so")

    def __init__(self) -> None:
        assert os.path.exists(self.LIB_PATH)
        lib = cdll.LoadLibrary(self.LIB_PATH)
        lib.ilmsens_hal_initHAL()

    def get_serial_number(self):
        return "serial_number"


