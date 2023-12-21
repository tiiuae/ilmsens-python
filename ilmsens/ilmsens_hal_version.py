from ctypes import c_uint


class ilmsens_hal_version:
    # major version number of HAL API
    ILMSENS_HAL_API_VER_MAJOR = c_uint(1)
    # minor version number of HAL API
    ILMSENS_HAL_API_VER_MINOR = c_uint(1)
    # build number of HAL API
    ILMSENS_HAL_API_VER_BUILD = c_uint(1)
    # single version number for preprocessors
    # ILMSENS_HAL_API_VER = (ILMSENS_HAL_API_VER_MAJOR * 100000 + ILMSENS_HAL_API_VER_MINOR * 1000 + ILMSENS_HAL_API_VER_BUILD)
    ILMSENS_HAL_API_VER = c_uint(101001)
