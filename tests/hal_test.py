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

# res = ilmsens_hal.initHAL()
# print(res)
# res = ilmsens_hal.getVersion()
# print(res.mMajor, res.mMinor, res.mBuild)

# ilmsens_hal.utils.drPropDependencies()
