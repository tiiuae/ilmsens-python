import atexit
import argparse
from ilmsens_hal import ilmsens_hal
from ilmsens_hal import ilmsens_hal_config
from ilmsens_hal import ilmsens_hal_meas_run
from ilmsens_hal import ilmsens_hal_meas_config
from ilmsens_hal import ilmsens_hal_ModConfig


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
    c = ilmsens_hal()
    selected_sensor = 0
    num_sensors = c.ilmsens_hal_initHAL()
    sensors_list = [i+1 for i in range(num_sensors)]

    atexit.register(c.ilmsens_hal_closeSensors, sensors_list)
    atexit.register(c.ilmsens_hal_deinitHAL)

    c.ilmsens_hal_setDEBLevel(args.logLevel)
    ver = c.ilmsens_hal_getVersion()
    print(f"HAL library version is V{ver.mMajor}.{ver.mMinor}.{ver.mBuild}")
    print(f"HAL library detected {num_sensors} sensors.")
    c.ilmsens_hal_openSensors(sensors_list)

    for i in sensors_list:
        id = c.ilmsens_hal_getModId(i)
        print(f"Sensor #1 has ID '{id.decode()}' (result was {len(id)}).")

    c.ilmsens_hal_setMaster(sensors_list, ilmsens_hal_config.ILMSENS_HAL_SLAVE_SENSOR)
    c.ilmsens_hal_closeSensors(sensors_list)


    c.ilmsens_hal_openSensors([sensors_list[selected_sensor]])

    config = ilmsens_hal_ModConfig()
    config.mClk = args.rfClock
    config.mOV = 0 # 0 = use default
    config.mOrder = args.mlbsOrder
    config.mRx = 2
    config.mSub = 0 # 0 = use default
    config.mTx = 0 # 0 = use default

    c.ilmsens_hal_setupSensors([sensors_list[selected_sensor]], config)
    c.ilmsens_hal_setMaster([sensors_list[selected_sensor]], ilmsens_hal_config.ILMSENS_HAL_MASTER_SENSOR)

    c.ilmsens_hal_synchMS([sensors_list[selected_sensor]], ilmsens_hal_meas_config.ILMSENS_HAL_SYNCH_OFF)
    c.ilmsens_hal_synchMS([sensors_list[selected_sensor]], ilmsens_hal_meas_config.ILMSENS_HAL_SYNCH_ON)

    c.ilmsens_hal_setMLBS([sensors_list[selected_sensor]])
    c.ilmsens_hal_setAvg([sensors_list[selected_sensor]], 1, 0)

    tSenInfo = c.ilmsens_hal_getModInfo(sensors_list[selected_sensor])
    c.ilmsens_hal_setPD([sensors_list[selected_sensor]], ilmsens_hal_meas_config.ILMSENS_HAL_TX_ON)

    print()
    print("Configuration of selected sensor is :")
    print("* RF system clock    [GHz]: {:.6f}".format(tSenInfo.mConfig.mClk))
    print("* MLBS order              : {}".format(tSenInfo.mConfig.mOrder))
    print("* Prescaler           1/  : {}".format(tSenInfo.mConfig.mSub))
    print("* Oversampling        x   : {}".format(tSenInfo.mConfig.mOV))
    print("* Number of Tx            : {}".format(tSenInfo.mConfig.mTx))
    print("* Number of Rx            : {}".format(tSenInfo.mConfig.mRx))
    print("* Number of samples per Rx: {}".format(tSenInfo.mNumSamp))
    print("* Hardware averages       : {}".format(tSenInfo.mHWAvg))
    print("* Software avg. limits    : [{} .. {}]".format(tSenInfo.mAvgLim[0], tSenInfo.mAvgLim[1]))
    print("* Software averages       : {}".format(tSenInfo.mAvg))
    print("* Wait cycle limits       : [{} .. {}]".format(tSenInfo.mWaitLim[0], tSenInfo.mWaitLim[1]))
    print("* Wait cycles             : {}".format(tSenInfo.mWait))
    print("* ADC full scale range [V]: [{:.6f} .. {:.6f}]".format(tSenInfo.mFSR[0], tSenInfo.mFSR[1]))
    print("* ADC LSB voltage     [mV]: {:.6f}".format(tSenInfo.mLSB_Volt*1000.0))
    print("* Int. temperature    [\370C]: {:.2f}".format(tSenInfo.mTemp))
    print()

    tRxSize  = tSenInfo.mNumSamp + tSenInfo.mConfig.mOV
    tBufSize = 1 * tRxSize * tSenInfo.mConfig.mRx

    for _ in range(args.repeatCount):
        c.ilmsens_hal_measRun([sensors_list[selected_sensor]], ilmsens_hal_meas_run.ILMSENS_HAL_RUN_BUF)

        for i in range(args.responseCount):
            d = c.ilmsens_hal_measGet([sensors_list[selected_sensor]], timeout_millis=args.timeoutMillis)
            print(f"Received impulse response #{i+1}")




if __name__ == "__main__":
    args = get_inline_arguments()
    hal_itest(args)
