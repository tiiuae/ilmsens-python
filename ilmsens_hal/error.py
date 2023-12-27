from ctypes import c_int


# No error
ILMSENS_SUCCESS = c_int(0)
# Invalid parameter
ILMSENS_ERROR_INVALID_PARAM = c_int(-1)
# Invalid state (e.g. on reading data, when no measurement is running)
ILMSENS_ERROR_STATE = c_int(-2)
# Ressource is busy
ILMSENS_ERROR_BUSY = c_int(-3)
# Access denied
ILMSENS_ERROR_ACCESS = c_int(-4)
# Input/Output error (e.g. transmission error or device disconnected)
ILMSENS_ERROR_IO = c_int(-5)
# Ressource allocation failed
ILMSENS_ERROR_NO_MEMORY = c_int(-6)
# Not enough data, try again later (e.g. when a non-blocking operation would need to block the caller)
ILMSENS_ERROR_AGAIN = c_int(-7)
# Timeout expired
ILMSENS_ERROR_TIMEOUT = c_int(-8)
# Operation not supported
ILMSENS_ERROR_NOT_SUPPORTED = c_int(-9)
# Unspecified error
ILMSENS_ERROR_UNKNOWN = c_int(-99)
