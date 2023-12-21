import atexit
import argparse
from ilmsens_hal import ilmsens_hal


def get_inline_arguments():
    parser = argparse.ArgumentParser(description="Run Ilmsens m:explore measurement test using the HAL API Python wrapper.")

    parser.add_argument(
        '--mlbsOrder',
        type=int,
        default=9,
        help="M-sequence order of the sensor. Values: (9, 12, or 15)")
    parser.add_argument(
        '--rfClock',
        type=float,
        default=13.312,
        help="RF clock rate of the sensor [GHz]. Values: (0.1 .. 18.0)")
    parser.add_argument(
        '--softwareAvg',
        type=int,
        default=32,
        help="Software averages done for each impulse response acquired. Values: (1 .. 4096)")
    parser.add_argument(
        '--repeatCount',
        type=int,
        default=1,
        help="Number of test measurement runs. Values: (1 .. MAX_UINT32)")
    parser.add_argument(
        '--responseCount',
        type=int,
        default=10,
        help="Number of impulse responses acquired per test measurement run. Values: (1 .. MAX_UINT32)")
    parser.add_argument(
        '--timeoutMillis',
        type=int,
        default=500,
        help="Timeout [ms] the application waits between impulse responses. Values: (0 .. MAX_UINT32)")
    parser.add_argument(
        '--logLevel',
        type=int,
        default=2,
        help="Set log verbosity of HAL integration test application. Values: (0 .. 4)")
    parser.add_argument(
        '--bufferedMode',
        action='store_true',
        help="If this command line flag is specified, the measurement \
            uses buffered (threaded) mode. Otherwise raw mode is used.")

    return parser.parse_args()


def hal_itest(args=None):
    print("hal_itest")
    pass
    # c = uwb_hal()
    # atexit.register(c.ilmsens_hal_closeSensors, [1])
    # atexit.register(c.ilmsens_hal_deinitHAL)

    # selected_sensor = 0

    # num_sensors = c.ilmsens_hal_initHAL()
    # c.ilmsens_hal_setDEBLevel(args.logLevel)
    # ver = c.ilmsens_hal_getVersion()
    # print(f"HAL library version is V{ver.mMajor}.{ver.mMinor}.{ver.mBuild}")
    # print(f"HAL library detected {num_sensors} sensors.")

    # sensors_list = [i+1 for i in range(num_sensors)]
    # c.ilmsens_hal_openSensors(sensors_list)

    # for i in sensors_list:
    #     id = c.ilmsens_hal_getModId(i)
    #     print(f"Sensor #1 has ID '{id.decode()}' (result was {len(id)}).")

    # c.ilmsens_hal_setMaster(sensors_list, ilmsens_hal_Modes.ILMSENS_HAL_SLAVE_SENSOR)
    # c.ilmsens_hal_closeSensors(sensors_list)


    # c.ilmsens_hal_openSensors([sensors_list[selected_sensor]])
    # c.ilmsens_hal_setMaster([sensors_list[selected_sensor]], ilmsens_hal_Modes.ILMSENS_HAL_MASTER_SENSOR)

    # c.ilmsens_hal_synchMS([sensors_list[selected_sensor]], ilmsens_hal_SynchModes.ILMSENS_HAL_SYNCH_OFF)
    # c.ilmsens_hal_synchMS([sensors_list[selected_sensor]], ilmsens_hal_SynchModes.ILMSENS_HAL_SYNCH_ON)

    # c.ilmsens_hal_setMLBS([sensors_list[selected_sensor]])
    # c.ilmsens_hal_setAvg([sensors_list[selected_sensor]], args.softwareAvg, 0)

    # info = c.ilmsens_hal_getModInfo(sensors_list[selected_sensor])
    # print("\nConfig")
    # print(*[(x, getattr(info.mConfig, x)) for x in dir(info.mConfig) if x[0] == 'm'], sep='\n')
    # print("\nInfo")
    # print(*[(x, getattr(info, x)) for x in dir(info) if x[0] == 'm'], sep='\n')

    # c.ilmsens_hal_setPD([sensors_list[selected_sensor]], ilmsens_hal_PowerModes.ILMSENS_HAL_TX_ON)

    # for _ in range(args.repeatCount):
    #     c.ilmsens_hal_measRun([sensors_list[selected_sensor]], ilmsens_hal_MeasModes.ILMSENS_HAL_RUN_BUF)

    #     for i in range(args.responseCount):
    #         d = c.ilmsens_hal_measGet([sensors_list[selected_sensor]], args.timeoutMillis)
    #         print(f"Received impulse response #{i+1}")




if __name__ == "__main__":
    args = get_inline_arguments()
    hal_itest(args)
