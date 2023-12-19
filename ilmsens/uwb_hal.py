import os
import time
from typing import List
from ctypes import *


class ilmsens_hal_Version(Structure):
    _fields_ = [("mMajor", c_uint),
                ("mMinor", c_uint),
                ("mBuild", c_uint)]

class ilmsens_hal_ModConfig(Structure):
    _fields_ = [("mOrder", c_uint),
                ("mSub", c_uint),
                ("mClk", c_double),
                ("mOV", c_uint),
                ("mTx", c_uint),
                ("mRx", c_uint)]

class ilmsens_hal_ModInfo(Structure):
    _fields_ = [("mConfig", ilmsens_hal_ModConfig),
                ("mTB_Fc", c_double),
                ("mTemp", c_double),
                ("mLSB_Volt", c_double),
                ("mFSR", c_double),
                ("mHWAvg", c_uint),
                ("mAvg", c_uint),
                ("mAvgLim", c_uint),
                ("mWait", c_uint),
                ("mWaitLim", c_uint),
                ("mNumSamp", c_uint)]

class ilmsens_hal_DEBLevels:
    ILMSENS_DEB_NO = c_uint(0)
    ILMSENS_DEB_INFO = c_uint(1)
    ILMSENS_DEB_MORE = c_uint(2)
    ILMSENS_DEB_MOST = c_uint(3)
    ILMSENS_DEB_ALL = c_uint(4)

class ilmsens_hal_Modes:
    ILMSENS_HAL_SLAVE_SENSOR = c_int(0)
    ILMSENS_HAL_MASTER_SENSOR = c_int(1)

class ilmsens_hal_SynchModes:
    ILMSENS_HAL_SYNCH_OFF = c_int(0)
    ILMSENS_HAL_SYNCH_ON = c_int(1)

class ilmsens_hal_PowerModes:
    ILMSENS_HAL_TX_ON = c_int(0)
    ILMSENS_HAL_TX_OFF = c_int(1)

class ilmsens_hal_MeasModes:
    # sensor is currently not measuring
    ILMSENS_HAL_RUN_OFF = c_int(0)
    # sensor is measuring and data is not buffered by API
    ILMSENS_HAL_RUN_RAW = c_int(1)
    # sensor is measuring and data is buffered by API in separate thread
    ILMSENS_HAL_RUN_BUF = c_int(2)


class uwb_hal():

    LIB_PATH = os.path.join("/", "usr", "lib", "libilmsens_hal.so")
    ILMSENS_HAL_MOD_ID_BUF_SIZE = 1024
    ILMSENS_HAL_API_VER_MAJOR = 1
    ILMSENS_HAL_API_VER_MINOR = 1
    ILMSENS_HAL_API_VER_BUILD = 1
    ILMSENS_HAL_API_VER = 101001

    ilmsens_hal_SampleType = c_int32

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
        buffer_size = 100
        buffer = create_string_buffer(b"", buffer_size*4)
        rt = self.lib.ilmsens_hal_getModId(
            c_uint(dev_num),
            byref(buffer),
            c_size_t(buffer_size)
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

    def ilmsens_hal_measGet(self, dev_nums: List[int], timeout_millis: int) -> str:
        """ Blocks and reads the measurement data for all specified devices when it becomes available.
        This functions blocks the caller until at least one complete measurement is available for every device or a specified timeout expired.
        The buffer pBuffer must be large enough to hold one complete dataset for each device,
        i.e. it must be able to hold at least pNum complete datasets.

        Note: if pTimeoutMillis is 0, this function will block forever.
        """
        buffer_size = 1*(54610+1)*2 # 1 * tRxSize * tSenInfo.mConfig.mRx
        # buffer_size = 200000 # 1 * tRxSize * tSenInfo.mConfig.mRx
        # buffer = create_string_buffer(b'', buffer_size*4)
        buffer = create_string_buffer(buffer_size*4)
        self.lib.ilmsens_hal_measGet(
            byref(c_uint(dev_nums[0])),
            c_uint(len(dev_nums)),
            byref(buffer),
            c_size_t(buffer_size),
            c_uint(timeout_millis)
        )
        return string_at(buffer)

    def ilmsens_hal_measRead(self, dev_nums: List[int]) -> int:
        """ Reads the measurement data for all specified devices in non-blocking way.
        This functions is not blocking and returns immediately with the next measurement
        data or an error-code if no data are available.
        """
        buffer_size = 1000
        buffer = create_string_buffer(0, buffer_size*4)
        self.lib.ilmsens_hal_measRead(
            byref(c_uint(dev_nums[0])),
            c_uint(len(dev_nums)),
            byref(buffer),
            c_size_t(buffer_size)
        )
        return string_at(buffer)


if __name__ == "__main__":
    import time
    import atexit

    c = uwb_hal()
    num_devices = c.ilmsens_hal_initHAL()
    print(f"Found {num_devices} Ilmsens device{'' if num_devices == 1 else 's'}!")

    atexit.register(c.ilmsens_hal_closeSensors, [1])
    atexit.register(c.ilmsens_hal_deinitHAL)

    print()
    c.ilmsens_hal_setDEBLevel(ilmsens_hal_DEBLevels.ILMSENS_DEB_ALL)

    v = c.ilmsens_hal_getVersion()
    print("\nVersion")
    print(f"{v.mMajor}.{v.mMinor}.{v.mBuild}")

    print()
    c.ilmsens_hal_openSensors([1])

    d = c.ilmsens_hal_getModId(1)
    print("\nID")
    print(d)

    info = c.ilmsens_hal_getModInfo(1)
    print("\nInfo")
    print(*[(x, getattr(info, x)) for x in dir(info) if x[0] == 'm'], sep='\n')

    print("\nConfig")
    print(*[(x, getattr(info.mConfig, x)) for x in dir(info.mConfig) if x[0] == 'm'], sep='\n')

    print()
    d = c.ilmsens_hal_setMaster([1], ilmsens_hal_Modes.ILMSENS_HAL_MASTER_SENSOR)
    print(d)

    print()
    d = c.ilmsens_hal_synchMS([1], ilmsens_hal_SynchModes.ILMSENS_HAL_SYNCH_ON)
    print(d)

    print()
    d = c.ilmsens_hal_setMLBS([1])
    print(d)

    print()
    d = c.ilmsens_hal_setPD([1], ilmsens_hal_PowerModes.ILMSENS_HAL_TX_ON)
    print(d)

    print()
    d = c.ilmsens_hal_setAvg([1], 32, 0)
    print(d)

    print()
    d = c.ilmsens_hal_measRun([1], ilmsens_hal_MeasModes.ILMSENS_HAL_RUN_BUF)
    print(d)

    # time.sleep(0.1)

    # print()
    # for i in range(1000):
    #     d = c.ilmsens_hal_measRdy([1])
    #     print(d)


    # print()
    # d = c.ilmsens_hal_measStop([1])
    # print(d)

    # print()
    # d = c.ilmsens_hal_measRdy([1])
    # print(d)

    print()
    d = c.ilmsens_hal_measGet([1], 500)
    print(d)

    # print()
    # d = []
    # while len(d) == 0:
    #     d = c.ilmsens_hal_measRead([1])
    # print(d)
