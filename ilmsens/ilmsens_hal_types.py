from ctypes import Structure
from ctypes import c_double
from ctypes import c_uint32
from ctypes import c_int32
from ctypes import c_uint


class ilmsens_hal_Version(Structure):
    _fields_ = [
        ("mMajor", c_uint), # major version number
        ("mMinor", c_uint), # minor version number
        ("mBuild", c_uint), # build number
    ]

class ilmsens_hal_ModConfig(Structure):
    _fields_ = [
        ("mOrder", c_uint), # MLBS order
        ("mSub", c_uint), # subsampling factor
        ("mClk", c_double), # master clock
        ("mOV", c_uint), # number of oversampling
        ("mTx", c_uint), # number of transmitters
        ("mRx", c_uint), # number of receivers
    ]

class ilmsens_hal_ModInfo(Structure):
    _fields_ = [
        ("mConfig", ilmsens_hal_ModConfig), # basic configuration of sensor
        ("mTB_Fc", c_double), # corner frequency for timebase calibration
        ("mTemp", c_double), # device temperature
        ("mLSB_Volt", c_double), # ADC LSB voltage (for calculating physical values out of raw data)
        ("mFSR", (c_double * 2)), # ADC full scale range (minimum and maximum value)
        ("mHWAvg", c_uint), # number of hardware averages (FPGA)
        ("mAvg", c_uint), # number of averages
        ("mAvgLim", (c_uint * 2)), # limits for averages (minimum and maximum value)
        ("mWait", c_uint), # number of wait cycles
        ("mWaitLim", (c_uint * 2)), # limits for wait cycles (minimum and maximum value)
        ("mNumSamp", c_uint), # number of samples per channel
    ]

# Represents the data type of raw measured data
ilmsens_hal_SampleType = c_int32

# Represents data type for register and memory access
ilmsens_hal_MemoryType = c_uint32
