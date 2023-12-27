from ctypes import cdll
from ctypes import byref
from ctypes import c_uint
from ctypes import sizeof
from ctypes import c_byte
from ctypes import c_size_t
from ctypes import create_string_buffer, string_at
from typing import List, Tuple
from .ilmsens_hal_types import *
from .ilmsens_hal_defn import *


"""Load cpp library"""
lib_name = "libilmsens_hal.so"
c_ilmsens_hal = cdll.LoadLibrary(lib_name)



def getVersion() -> ilmsens_hal_Version:
    """
    Return the HAL version.

    Parameters
    ----------
    None

    Returns
    -------
    ilmsens_hal_Version
        an ilmsens_hal_Version type object, or
        ILMSENS_SUCCESS on success, or
        negative error-code
    """
    global c_ilmsens_hal
    hal_ver = ilmsens_hal_Version()
    c_ilmsens_hal.ilmsens_hal_getVersion(byref(hal_ver))
    return hal_ver



def setDEBLevel(level: c_uint) -> int:
    """
    Sets the verbosity of the diagnostics output Diagnostics are sent to std.
    error output by default. In case of an error, the current level is not changed.

    Parameters
    ----------
    level : int
        verbosity level from ILMSENS_DEB_NO to ILMSENS_DEB_ALL

    Returns
    -------
    int
        current debug level (on success and error)
    """
    return c_ilmsens_hal.ilmsens_hal_setDEBLevel(level)



def initHAL() -> int:
    """
    Initializes the library.
    This function must be called before calling any other library function.

    Parameters
    ----------
    None

    Returns
    -------
    int
        number of connected devices, or
        negative error-code

    """
    num_devices = c_ilmsens_hal.ilmsens_hal_initHAL()
    return num_devices



def deinitHAL() -> None:
    """
    Deinitializes the library.
    Should be called after closing all open devices and before your application terminates.
    This function always succeeds. Errors that appeared, will only be visible when calling ilmsens_hal_initHAL() again
    (i.e. if the library is not unloaded but a new session is started).
    """
    c_ilmsens_hal.ilmsens_hal_deinitHAL()



def openSensors(dev_nums: List[int]) -> int:
    """
    Allocates specified devices for a measurement session.
    This function must be called before doing the configuration or starting a measurement session.
    """
    c_ilmsens_hal.ilmsens_hal_openSensors(
        byref(c_uint(dev_nums[0])),
        c_uint(len(dev_nums))
    )



def closeSensors(dev_nums: List[int]) -> None:
    """
    Releases specified devices.
    Should be called after the last function call to any of the specified devices.
    """
    c_ilmsens_hal.ilmsens_hal_closeSensors(
        byref(c_uint(dev_nums[0])),
        c_uint(len(dev_nums))
    )



def getModId(dev_num: int) -> str:
    """
    Gets unique device-identifier.
    """
    buffer_size = 128
    buffer = create_string_buffer(buffer_size)
    _ = c_ilmsens_hal.ilmsens_hal_getModId(
        c_uint(dev_num),
        byref(buffer),
        c_size_t(len(buffer))
    )
    return string_at(buffer)



def getModInfo(dev_num: int) -> int:
    """
    Gets device hardware-configuration.
    """
    mod_info = ilmsens_hal_ModInfo()
    c_ilmsens_hal.ilmsens_hal_getModInfo(
        c_uint(dev_num),
        byref(mod_info)
    )
    return mod_info



def setupSensors(dev_nums: List[int], config: ilmsens_hal_ModConfig) -> int:
    """
    Performs the initial setup of specified devices.
    This function must be called before starting a measurement session.
    """
    c_ilmsens_hal.ilmsens_hal_setupSensors(
        byref(c_uint(dev_nums[0])),
        c_uint(len(dev_nums)),
        byref(config)
    )



def setMaster(dev_nums: List[int], mode: c_int) -> int:
    """
    Sets master/slave operational mode.
    Application needs to make sure, that any independent sensor is set to master mode.
    For hardware-synchronized operation of multiple sensors, exactly one sensor of a connected group has
    to be master the others in teh group must be configured as slaves.
    """
    res = c_ilmsens_hal.ilmsens_hal_setMaster(
        byref(c_uint(dev_nums[0])),
        c_uint(len(dev_nums)),
        mode
    )
    return res



def setAvg(dev_nums: List[int], avg: int, wait_cyc: int) -> int:
    """
    Sets software averages and wait cycles.
    Software averages define the acquisition aperture duration.
    If wait cycles are set to 0, devices measure in continuous mode.
    If wait cycles are non-zero, devices measure in snapshot mode.

    Note: May only be called when no measurement is running!
    """
    res = c_ilmsens_hal.ilmsens_hal_setAvg(
        byref(c_uint(dev_nums[0])),
        c_uint(len(dev_nums)),
        c_uint(avg),
        c_uint(wait_cyc)
    )
    return res



def setMLBS(dev_nums: List[int]) -> int:
    """
    Resets the M-sequence generator (transmitter) of each device.
    After digital synchronisation, the M-sequence generator (transmitter) of each device should be reset
    to ensure repeatable alignment of the transmitters and receivers.
    The reset typically takes a few ms to complete and cannot be used to mute the transmitter(s).

    Note: May only be called when no measurement is running!
    """
    res = c_ilmsens_hal.ilmsens_hal_setMLBS(
        byref(c_uint(dev_nums[0])),
        c_uint(len(dev_nums))
    )
    return res



def setPD(dev_nums: List[int], mode: c_int) -> int:
    """
    Controls the power-status of the transmitter.

    Note: May only be called when no measurement is running!
    """
    res = c_ilmsens_hal.ilmsens_hal_setPD(
        byref(c_uint(dev_nums[0])),
        c_uint(len(dev_nums)),
        mode
    )
    return res



def synchMS(dev_nums: List[int], mode: c_int) -> int:
    """
    Performs digital synchronisation.
    Must be used at least once before a measurement is started.
    """
    res = c_ilmsens_hal.ilmsens_hal_synchMS(
        byref(c_uint(dev_nums[0])),
        c_uint(len(dev_nums)),
        mode
    )
    return res



def measRun(dev_nums: List[int], mode: c_int) -> int:
    """
    Starts a measurement run with specified devices.
    One measurement run may be pending at a time.
    """
    res = c_ilmsens_hal.ilmsens_hal_measRun(
        byref(c_uint(dev_nums[0])),
        c_uint(len(dev_nums)),
        mode
    )
    return res



def measStop(dev_nums: List[int]) -> int:
    """
    Stops running measurement.
    """
    res = c_ilmsens_hal.ilmsens_hal_measStop(
        byref(c_uint(dev_nums[0])),
        c_uint(len(dev_nums))
    )
    return res



def measRdy(dev_nums: List[int]) -> int:
    """
    Reads the fill-level of the internal ring-buffer for all specified devices.
    This functions is not blocking and returns immediately. However, in raw mode, it will transfer data from a device to
    the libraries' ring-buffer on the host, if it discovers that a complete dataset is available.
    """
    res = c_ilmsens_hal.ilmsens_hal_measRdy(
        byref(c_uint(dev_nums[0])),
        c_uint(len(dev_nums))
    )
    return res



def measRead(dev_nums: List[int], buf_size_bytes: int = 4096) -> int:
    """
    Reads the measurement data for all specified devices in non-blocking way.
    This functions is not blocking and returns immediately with the next measurement
    data or an error-code if no data are available.
    """
    buffer = (c_byte * buf_size_bytes)(*([0x0] * buf_size_bytes))
    num_elements = c_ilmsens_hal.ilmsens_hal_measRead(
        byref(c_uint(dev_nums[0])),
        c_uint(len(dev_nums)),
        byref(buffer),
        c_size_t(len(bytes(buffer)))
    )
    return num_elements, bytes(buffer)



def measGet(dev_nums: List[int], buf_size_bytes: int = 4096, timeout_millis: int = 500) -> str:
    """
    Blocks and reads the measurement data for all specified devices when it becomes available.
    This functions blocks the caller until at least one complete measurement is available for every device or a specified timeout expired.
    The buffer pBuffer must be large enough to hold one complete dataset for each device,
    i.e. it must be able to hold at least pNum complete datasets.

    Note: if pTimeoutMillis is 0, this function will block forever.
    """
    buffer = (c_byte * buf_size_bytes)(*([0x0] * buf_size_bytes))
    num_elements = c_ilmsens_hal.ilmsens_hal_measGet(
        byref(c_uint(dev_nums[0])),
        c_uint(len(dev_nums)),
        byref(buffer),
        c_size_t(len(bytes(buffer))),
        c_uint(timeout_millis)
    )
    return bytes(buffer), num_elements



def readReg(dev_nums: List[int], reg: int) -> Tuple[int, bytes]:
    """
    Reads value from register at pReg address from all specified devices to buffer.
    The buffer pVal must be large enough to hold one word for each device, i.e. it must be at least pNum words in size.

    Parameters
    ----------
    dev_nums : List[int]
        an array of device-indexes
    reg : int
        register address
    """
    buf_size_bytes = len(dev_nums) * 4
    s = sizeof(ilmsens_hal_MemoryType)
    buffer = (ilmsens_hal_MemoryType * (buf_size_bytes//s))(*([0] * (buf_size_bytes//s)))
    num_elements = c_ilmsens_hal.ilmsens_hal_readReg(
        byref(c_uint(dev_nums[0])),
        c_uint(len(dev_nums)),
        c_uint(reg),
        byref(buffer),
        c_size_t(len(bytes(buffer)))
    )
    return bytes(buffer), num_elements



def writeReg(dev_nums: List[int], reg: int, val: int) -> int:
    """
    Writes pVal value to register at pReg address to all specified devices.
    The same value is written to each device.

    Parameters
    ----------
    dev_nums : List[int]
        an array of device-indexes
    reg : int
        register address
    val : int
        new register value
    """
    res = c_ilmsens_hal.ilmsens_hal_writeReg(
        byref(c_uint(dev_nums[0])),
        c_uint(len(dev_nums)),
        c_uint(reg),
        ilmsens_hal_MemoryType(val)
    )
    return res



def readBlk(dev_nums: List[int], adr: int, num_el: int) -> Tuple[int, bytes]:
    """
    Reads pNumEl elements (32-bit words) starting at address pAdr from the internal memory of specified devices into a buffer pVal.
    The buffer must be large enough to hold pNumEl words for all specified devices, i.e. it provide space for at least pNumEl x pNum words.

    Parameters
    ----------
    dev_nums : List[int]
        an array of device-indexes
    adr : int
        word-aligned start memory address
    num_el : int
        number of words (elements) to read
    """
    buf_size_bytes = len(dev_nums) * num_el * 4
    s = sizeof(ilmsens_hal_MemoryType)
    buffer = (ilmsens_hal_MemoryType * (buf_size_bytes//s))(*([0] * (buf_size_bytes//s)))
    num_elements = c_ilmsens_hal.ilmsens_hal_readBlk(
        byref(c_uint(dev_nums[0])),
        c_uint(len(dev_nums)),
        c_uint(adr),
        c_uint(num_el),
        byref(buffer),
        c_size_t(len(bytes(buffer)))
    )
    return num_elements, bytes(buffer)



def writeBlk(dev_nums: List[int], adr: int, num_el: int, val: List[int]) -> int:
    """
    Writes pNumEl elements (32-bit words) from buffer pVal to internal memory starting at address pAdr of specified devices.
    The same content is written to each device, i.e. the buffer pVal must hold pNumEl words regardless of pNum.

    Parameters
    ----------
    dev_nums : List[int]
        an array of device-indexes
    adr : int
        word-aligned start memory address
    num_el : int
        number of words (elements) to write
    val : List[int]
        a list with data to write
    """
    s = sizeof(ilmsens_hal_MemoryType)
    buffer = (ilmsens_hal_MemoryType * (len(val)//s))(*(val))
    res = c_ilmsens_hal.ilmsens_hal_writeReg(
        byref(c_uint(dev_nums[0])),
        c_uint(len(dev_nums)),
        c_uint(adr),
        c_uint(num_el),
        byref(bytes(val)),
        c_size_t(len(val * s))
    )
    return res
