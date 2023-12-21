from ctypes import c_int
from ctypes import c_uint


class ilmsens_hal_meas_run:
    # sensor is currently not measuring
    ILMSENS_HAL_RUN_OFF = c_int(0)
    # sensor is measuring and data is not buffered by API
    ILMSENS_HAL_RUN_RAW = c_int(1)
    # sensor is measuring and data is buffered by API in separate thread
    ILMSENS_HAL_RUN_BUF = c_int(2)

class ilmsens_hal_modinfo:
    # maximum length buffer size for retrieving the unique ID string
    ILMSENS_HAL_MOD_ID_BUF_SIZE = c_int(1024)

class ilmsens_hal_config:
    # setup the sensor(s) to be slave devices
    ILMSENS_HAL_SLAVE_SENSOR = c_int(0)
    # setup the sensor(s) to be master devices
    ILMSENS_HAL_MASTER_SENSOR = c_int(1)

class ilmsens_hal_meas_config:
    # retract digital synchronisation, i.e. sensors will be unsynch'ed
    ILMSENS_HAL_SYNCH_OFF = c_int(0)
    # perform digital synchronisation, i.e. sensors will be synch'ed
    ILMSENS_HAL_SYNCH_ON = c_int(1)
    # transmitter is in power down mode, i.e. output amplifier is switch off
    ILMSENS_HAL_TX_OFF = c_int(1)
    # transmitter is working, i.e. output amplifier is switched on
    ILMSENS_HAL_TX_ON = c_int(0)

class ilmsens_hal_diag:
    # do not output debug/info messages
    ILMSENS_DEB_NO = c_uint(0)
    # only output errors and very important information
    ILMSENS_DEB_INFO = c_uint(1)
    # output errors, warnings, and important information
    ILMSENS_DEB_MORE = c_uint(2)
    # output errors, warnings, and debug information
    ILMSENS_DEB_MOST = c_uint(3)
    # output errors, warnings, and trace information
    ILMSENS_DEB_ALL = c_uint(4)
