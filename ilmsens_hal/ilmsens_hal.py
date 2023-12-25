import os
import struct
from ctypes import *
from typing import List
from .ilmsens_hal_types import *
from .ilmsens_hal_defn import *


class ilmsens_hal():

    LIB_PATH = os.path.join("/", "usr", "lib", "libilmsens_hal.so")

    def __init__(self) -> None:
        assert os.path.exists(self.LIB_PATH), f"Can't find {self.LIB_PATH}"
        self.lib = cdll.LoadLibrary(self.LIB_PATH)

    def __del__(self) -> None:
        pass


    def ilmsens_hal_getVersion(self) -> ilmsens_hal_Version:
        hal_ver = ilmsens_hal_Version()
        self.lib.ilmsens_hal_getVersion(byref(hal_ver))
        return hal_ver

    def ilmsens_hal_setDEBLevel(self, level: c_uint) -> int:
        return self.lib.ilmsens_hal_setDEBLevel(level)

    def ilmsens_hal_initHAL(self) -> int:
        num_devices = self.lib.ilmsens_hal_initHAL()
        return num_devices

    def ilmsens_hal_deinitHAL(self) -> None:
        self.lib.ilmsens_hal_deinitHAL()

    def ilmsens_hal_setupSensors(self, dev_nums: List[int], config: ilmsens_hal_ModConfig) -> int:
        self.lib.ilmsens_hal_setupSensors(
            byref(c_uint(dev_nums[0])),
            c_uint(len(dev_nums)),
            byref(config)
        )

    def ilmsens_hal_openSensors(self, dev_nums: List[int]) -> int:
        self.lib.ilmsens_hal_openSensors(
            byref(c_uint(dev_nums[0])),
            c_uint(len(dev_nums))
        )

    def ilmsens_hal_closeSensors(self, dev_nums: List[int]) -> None:
        self.lib.ilmsens_hal_closeSensors(
            byref(c_uint(dev_nums[0])),
            c_uint(len(dev_nums))
        )

    def ilmsens_hal_getModId(self, dev_num: int) -> str:
        buffer_size = 128
        buffer = create_string_buffer(buffer_size)
        _ = self.lib.ilmsens_hal_getModId(
            c_uint(dev_num),
            byref(buffer),
            c_size_t(len(buffer))
        )
        return string_at(buffer)

    def ilmsens_hal_getModInfo(self, dev_num: int) -> int:
        mod_info = ilmsens_hal_ModInfo()
        self.lib.ilmsens_hal_getModInfo(
            c_uint(dev_num),
            byref(mod_info)
        )
        return mod_info

    def ilmsens_hal_setMaster(self, dev_nums: List[int], mode: c_int) -> int:
        rt = self.lib.ilmsens_hal_setMaster(
            byref(c_uint(dev_nums[0])),
            c_uint(len(dev_nums)),
            mode
        )
        return rt

    def ilmsens_hal_synchMS(self, dev_nums: List[int], mode: c_int) -> int:
        rt = self.lib.ilmsens_hal_synchMS(
            byref(c_uint(dev_nums[0])),
            c_uint(len(dev_nums)),
            mode
        )
        return rt

    def ilmsens_hal_setMLBS(self, dev_nums: List[int]) -> int:
        rt = self.lib.ilmsens_hal_setMLBS(
            byref(c_uint(dev_nums[0])),
            c_uint(len(dev_nums))
        )
        return rt

    def ilmsens_hal_setPD(self, dev_nums: List[int], mode: c_int) -> int:
        rt = self.lib.ilmsens_hal_setPD(
            byref(c_uint(dev_nums[0])),
            c_uint(len(dev_nums)),
            mode
        )
        return rt

    def ilmsens_hal_setAvg(self, dev_nums: List[int], avg: int, wait_cyc: int) -> int:
        """ Sets software averages and wait cycles.
        Software averages define the acquisition aperture duration.
        If wait cycles are set to 0, devices measure in continuous mode.
        If wait cycles are non-zero, devices measure in snapshot mode.

        Note: May only be called when no measurement is running!
        """
        rt = self.lib.ilmsens_hal_setAvg(
            byref(c_uint(dev_nums[0])),
            c_uint(len(dev_nums)),
            c_uint(avg),
            c_uint(wait_cyc)
        )
        return rt

    def ilmsens_hal_measRun(self, dev_nums: List[int], mode: c_int) -> int:
        """ Starts a measurement run with specified devices.
        One measurement run may be pending at a time.
        """
        rt = self.lib.ilmsens_hal_measRun(
            byref(c_uint(dev_nums[0])),
            c_uint(len(dev_nums)),
            mode
        )
        return rt

    def ilmsens_hal_measStop(self, dev_nums: List[int]) -> int:
        """ Stops running measurement.
        """
        rt = self.lib.ilmsens_hal_measStop(
            byref(c_uint(dev_nums[0])),
            c_uint(len(dev_nums))
        )
        return rt

    def ilmsens_hal_measRdy(self, dev_nums: List[int]) -> int:
        """ Reads the fill-level of the internal ring-buffer for all specified devices.
        This functions is not blocking and returns immediately. However, in raw mode, it will transfer data from a device to
        the libraries' ring-buffer on the host, if it discovers that a complete dataset is available.
        """
        rt = self.lib.ilmsens_hal_measRdy(
            byref(c_uint(dev_nums[0])),
            c_uint(len(dev_nums))
        )
        return rt

    def ilmsens_hal_measGet(self, dev_nums: List[int], buf_size_bytes: int = 4096, timeout_millis: int = 500) -> str:
        """ Blocks and reads the measurement data for all specified devices when it becomes available.
        This functions blocks the caller until at least one complete measurement is available for every device or a specified timeout expired.
        The buffer pBuffer must be large enough to hold one complete dataset for each device,
        i.e. it must be able to hold at least pNum complete datasets.

        Note: if pTimeoutMillis is 0, this function will block forever.
        """
        buffer = (c_byte * buf_size_bytes)(*([0x0] * buf_size_bytes))
        num_elements = self.lib.ilmsens_hal_measGet(
            byref(c_uint(dev_nums[0])),
            c_uint(len(dev_nums)),
            byref(buffer),
            c_size_t(len(bytes(buffer))),
            c_uint(timeout_millis)
        )
        return num_elements, bytes(buffer)

    def ilmsens_hal_measRead(self, dev_nums: List[int], buf_size_bytes: int = 4096) -> int:
        """ Reads the measurement data for all specified devices in non-blocking way.
        This functions is not blocking and returns immediately with the next measurement
        data or an error-code if no data are available.
        """
        buffer = (c_byte * buf_size_bytes)(*([0x0] * buf_size_bytes))
        num_elements = self.lib.ilmsens_hal_measRead(
            byref(c_uint(dev_nums[0])),
            c_uint(len(dev_nums)),
            byref(buffer),
            c_size_t(len(bytes(buffer)))
        )
        return num_elements, bytes(buffer)

    def ilmsens_hal_readReg(self, dev_nums: List[int], reg: int) -> int:
        buffer_size = len(dev_nums)
        buffer = (c_int16 * buffer_size)(*([0] * buffer_size))
        _ = self.lib.ilmsens_hal_measGet(
            byref(c_uint(dev_nums[0])),
            c_uint(len(dev_nums)),
            c_uint(reg),
            byref(buffer),
            c_size_t(len(bytes(buffer)))
        )
        return bytes(buffer)

    def ilmsens_hal_writeReg(self, dev_nums: List[int]) -> int:
        pass

    def ilmsens_hal_readBlk(self, dev_nums: List[int]) -> int:
        pass

    def ilmsens_hal_writeBlk(self, dev_nums: List[int]) -> int:
        pass

    @staticmethod
    def parse_data(buffer) -> tuple:
        rx1_samples = buffer[:2044]
        seq_counter = buffer[2044:2048]
        rx2_samples = buffer[2048:4092]
        reserved = buffer[4092:]

        rx1_samples = struct.unpack("<%di" % (len(rx1_samples)//4), rx1_samples)
        rx2_samples = struct.unpack("<%di" % (len(rx2_samples)//4), rx2_samples)
        seq_counter = struct.unpack("<%di" % (len(seq_counter)//4), seq_counter)

        return {
            "seq_counter": seq_counter,
            "rx1_samples": rx1_samples,
            "rx2_samples": rx2_samples,
            "reserved": reserved
        }


# if __name__ == "__main__":
#     from tests import hal_itest
#     hal_itest()
