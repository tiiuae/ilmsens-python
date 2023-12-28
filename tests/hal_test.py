import atexit
import ilmsens_hal

import ilmsens_hal.error
from ilmsens_hal.error import ILMSENS_SUCCESS
from ilmsens_hal.error import ILMSENS_ERROR_INVALID_PARAM
from ilmsens_hal.error import ILMSENS_ERROR_STATE
from ilmsens_hal.error import ILMSENS_ERROR_BUSY
from ilmsens_hal.error import ILMSENS_ERROR_ACCESS
from ilmsens_hal.error import ILMSENS_ERROR_IO
from ilmsens_hal.error import ILMSENS_ERROR_NO_MEMORY
from ilmsens_hal.error import ILMSENS_ERROR_AGAIN
from ilmsens_hal.error import ILMSENS_ERROR_TIMEOUT
from ilmsens_hal.error import ILMSENS_ERROR_NOT_SUPPORTED
from ilmsens_hal.error import ILMSENS_ERROR_UNKNOWN

import ilmsens_hal.types
from ilmsens_hal.types import ilmsens_hal_Version
from ilmsens_hal.types import ilmsens_hal_ModConfig
from ilmsens_hal.types import ilmsens_hal_ModInfo
from ilmsens_hal.types import ilmsens_hal_SampleType
from ilmsens_hal.types import ilmsens_hal_MemoryType

import ilmsens_hal.defn
from ilmsens_hal.defn import meas_run
from ilmsens_hal.defn import modinfo
from ilmsens_hal.defn import meas_config
from ilmsens_hal.defn import config
from ilmsens_hal.defn import diag

import ilmsens_hal.utils


ver = ilmsens_hal.getVersion()
_ = ilmsens_hal.setDEBLevel(diag.ILMSENS_DEB_NO)
print(f"HAL Version: {ver.mMajor}.{ver.mMinor}.{ver.mBuild}")

num_devices = ilmsens_hal.initHAL()
connected_devices = list(range(1, num_devices+1))
print(f"Found {num_devices} connected devices")
_ = ilmsens_hal.openSensors(connected_devices)

atexit.register(ilmsens_hal.deinitHAL)
atexit.register(ilmsens_hal.closeSensors, connected_devices)

for idx in connected_devices:
    device_id = ilmsens_hal.getModId(idx)
    print(f"Sensor #{idx} has ID '{device_id.decode()}' (result was {len(device_id)}).")
print()

selected_device_idx = None
while selected_device_idx not in connected_devices:
    selected_device_idx = input("Select a device to connect to (Type the Sensor #, then press Enter): ")
    selected_device_idx = int(selected_device_idx)
print(f"* Selected Sensor #{selected_device_idx}")
print()

swavg = 3
wait_cyc = 0
mod_config = ilmsens_hal_ModConfig()
mod_config.mClk = 13.312
mod_config.mOV = 0 # 0 = use default
mod_config.mOrder = 9
mod_config.mRx = 2
mod_config.mSub = 0 # 0 = use default
mod_config.mTx = 0 # 0 = use default
ilmsens_hal.setupSensors([selected_device_idx], mod_config)
ilmsens_hal.setMaster([selected_device_idx], config.ILMSENS_HAL_MASTER_SENSOR)
ilmsens_hal.synchMS([selected_device_idx], meas_config.ILMSENS_HAL_SYNCH_OFF)
ilmsens_hal.synchMS([selected_device_idx], meas_config.ILMSENS_HAL_SYNCH_ON)
ilmsens_hal.setMLBS([selected_device_idx])
ilmsens_hal.setAvg([selected_device_idx], swavg, wait_cyc)

info = ilmsens_hal.getModInfo(selected_device_idx)
print("Configuration of selected sensor is :")
print("* RF system clock    [GHz]: {:.6f}".format(info.mConfig.mClk))
print("* MLBS order              : {}".format(info.mConfig.mOrder))
print("* Prescaler           1/  : {}".format(info.mConfig.mSub))
print("* Oversampling        x   : {}".format(info.mConfig.mOV))
print("* Number of Tx            : {}".format(info.mConfig.mTx))
print("* Number of Rx            : {}".format(info.mConfig.mRx))
print("* Number of samples per Rx: {}".format(info.mNumSamp))
print("* Hardware averages       : {}".format(info.mHWAvg))
print("* Software avg. limits    : [{} .. {}]".format(info.mAvgLim[0], info.mAvgLim[1]))
print("* Software averages       : {}".format(info.mAvg))
print("* Wait cycle limits       : [{} .. {}]".format(info.mWaitLim[0], info.mWaitLim[1]))
print("* Wait cycles             : {}".format(info.mWait))
print("* ADC full scale range [V]: [{:.6f} .. {:.6f}]".format(info.mFSR[0], info.mFSR[1]))
print("* ADC LSB voltage     [mV]: {:.6f}".format(info.mLSB_Volt*1000.0))
print("* Int. temperature    [\370C]: {:.2f}".format(info.mTemp))
print()


device_id = ilmsens_hal.getModId(selected_device_idx)
print(f"Sensor #{selected_device_idx} has ID '{device_id.decode()}' (result was {len(device_id)}).")
ilmsens_hal.setPD([selected_device_idx], meas_config.ILMSENS_HAL_TX_ON)
for _ in range(1):
    ilmsens_hal.measRun([selected_device_idx], meas_run.ILMSENS_HAL_RUN_BUF)

    for i in range(10):
        _ = ilmsens_hal.measGet([selected_device_idx], timeout_millis=100)
        print(f"Received impulse response #{i+1}")
