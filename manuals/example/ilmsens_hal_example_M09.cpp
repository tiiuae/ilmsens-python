/// @file ilmsens_hal_example.cpp
/// @brief Simple DEMO application for Ilmsens UWB HAL API
/// @author pavol.kurina@gmail.com and Ralf.Herrmann@ilmsens.com

//common headers
#include <cmath>
#include <iostream>
#include <iomanip>
#include <sstream>
#include <string>
#include <stdexcept>
#include <vector>
#include <chrono>

using namespace std::chrono;

//get the HAL
#include "ilmsens/hal/ilmsens_hal.h"


////////////////////////////////////////////////////////////////////////
// default sensor setup
////////////////////////////////////////////////////////////////////////

#define LOG_LEVEL_DEFAULT   ILMSENS_DEB_INFO //default log level for application

#define MLBS_ORDER_DEFAULT   9       //can be 9, 12, or 15 at the moment
#define MLBS_CLK_DEFAULT     13.312  //default master clock rate [GHz]
#define MLBS_NUM_RX_DEFAULT  2       //default number fo Rx per sensor

#define SW_AVG_DEFAULT       32      //default software averages
#define WAIT_CYC_DEFAULT      0      //default wait cycles (0 = no wait cycles used)

#define SENSOR_NUM_DEFAULT   1       //default sensor number to use for the application
#define REPEAT_CNT_DEFAULT   1       //default repeat count of test runs
#define REPONSE_CNT_DEFAULT  10      //default impulse response count per test run

#define TIMEOUT_MS_DEFAULT   500     //default timeout between IRFs [ms]


////////////////////////////////////////////////////////////////////////
// configuration variables
////////////////////////////////////////////////////////////////////////

//logging
static unsigned sLogLevel = LOG_LEVEL_DEFAULT;

//sensor parameters
static unsigned sMLBSOrder = MLBS_ORDER_DEFAULT;      
static double   sMasterClk = MLBS_CLK_DEFAULT; 
static unsigned sNumRx     = MLBS_NUM_RX_DEFAULT;

//measurement parameters
static unsigned sSWAvg    = SW_AVG_DEFAULT;    

//test run setup
static unsigned sSenNum   = SENSOR_NUM_DEFAULT;
static unsigned sRepCnt   = REPEAT_CNT_DEFAULT;
static unsigned sIRFCnt   = REPONSE_CNT_DEFAULT;

static unsigned sTOMillis = TIMEOUT_MS_DEFAULT;


////////////////////////////////////////////////////////////////////////
// helper functions
////////////////////////////////////////////////////////////////////////

//apply defaults to all config variables
void resetDefaults()
{
  //logging
  sLogLevel = LOG_LEVEL_DEFAULT;
  
  //sensor parameters
  sMLBSOrder = MLBS_ORDER_DEFAULT;      
  sMasterClk = MLBS_CLK_DEFAULT; 

  //measurement parameters
  sSWAvg    = SW_AVG_DEFAULT;    

  //test run setup
  sSenNum   = SENSOR_NUM_DEFAULT;
  sRepCnt   = REPEAT_CNT_DEFAULT;
  sIRFCnt   = REPONSE_CNT_DEFAULT;

  sTOMillis = TIMEOUT_MS_DEFAULT;
}

//parse command line to set various parameters
void parseCommandLine(unsigned argc, char* argv[])
{
  //apply defaults first
  resetDefaults();

  for (unsigned tI = 1; tI < argc; ++tI) 
  {
    if (0 == std::string("--mlbsOrder").compare(argv[tI])) 
    {
      if (tI + 1 < argc) 
      {
        sMLBSOrder = std::stoi(argv[tI + 1]);
      }
      else 
      {
        throw std::runtime_error("missing MLBS order argument.");
      }
    } 
    else if (0 == std::string("--rfClock").compare(argv[tI])) 
    {
      if (tI + 1 < argc) 
      {
        sMasterClk = std::stod(argv[tI + 1]);
      }
      else 
      {
        throw std::runtime_error("missing master clock [GHz] argument.");
      }
    } 
    else if (0 == std::string("--repeatCount").compare(argv[tI])) 
    {
      if (tI + 1 < argc) 
      {
        sRepCnt = std::stoi(argv[tI + 1]);
      }
      else 
      {
        throw std::runtime_error("missing repeat count argument.");
      }
    } 
    else if (0 == std::string("--sensorNum").compare(argv[tI])) 
    {
      if (tI + 1 < argc) 
      {
        sSenNum = std::stoi(argv[tI+1]);
      } 
      else
      {
        throw std::runtime_error("missing software averages argument.");
      }
    } 
    else if (0 == std::string("--softwareAvg").compare(argv[tI])) 
    {
      if (tI + 1 < argc) 
      {
        sSWAvg = std::stoi(argv[tI+1]);
      } 
      else
      {
        throw std::runtime_error("missing software averages argument.");
      }
    } 
    else if (0 == std::string("--responseCount").compare(argv[tI])) 
    {
      if (tI + 1 < argc) 
      {
        sIRFCnt = std::stoi(argv[tI+1]);
      } 
      else
      {
        throw std::runtime_error("missing impulse response count argument.");
      }
    } 
    else if (0 == std::string("--timeoutMillis").compare(argv[tI])) 
    {
      if (tI + 1 < argc) 
      {
        sTOMillis = std::stoi(argv[tI + 1]);
      } 
      else
      {
        throw std::runtime_error("missing timeout argument.");
      }
    } 
    else if (0 == std::string("--logLevel").compare(argv[tI])) 
    {
      if (tI + 1 < argc) 
      {
        sLogLevel = std::stoi(argv[tI + 1]);
      } 
      else
      {
        throw std::runtime_error("missing log level argument.");
      }
    } 
  }
}


////////////////////////////////////////////////////////////////////////
// useful macros
////////////////////////////////////////////////////////////////////////

#define HAL_CALL_ERROR_EXIT(pFuncCall, pErrMsg) \
  mHalResult = pFuncCall; \
  if (mHalResult < ILMSENS_SUCCESS) \
  { \
    std::cerr << pErrMsg << " Error code was: " << std::dec << mHalResult << std::endl; \
    ilmsens_hal_deinitHAL(); \
    return(2); \
  }


////////////////////////////////////////////////////////////////////////
// useful types
////////////////////////////////////////////////////////////////////////

typedef unsigned TSensorNumber;
typedef std::vector<TSensorNumber> TSensorNumbers;
typedef std::vector<ilmsens_hal_SampleType> TSampleBuffer;


////////////////////////////////////////////////////////////////////////
// data processing
////////////////////////////////////////////////////////////////////////


void processMLBSData(ilmsens_hal_ModInfo& /*pInfo*/, unsigned /*pNumSensors*/, TSampleBuffer& /*pBuffer*/)
{
  /* add the data processing here */
  std::cout << "<no processing defined>" << std::endl;
}

////////////////////////////////////////////////////////////////////////
// entry point for example application
////////////////////////////////////////////////////////////////////////

int main(int argc, char* argv[])
{
  //get config parameters from command line
  try
  {
    parseCommandLine(argc, argv);
  }
  catch (const std::runtime_error &tEx)
  {
    std::cerr << "Error parsing command line: " << tEx.what() << std::endl;
    return(1);
  }

  ////////////////////////////////////////////////////////////////////////
  // init the HAl and enumerate sensors
  ////////////////////////////////////////////////////////////////////////

  //remember HAL library return codes 
  //(this variable is also used in the error handling macro!)
  int mHalResult = ILMSENS_SUCCESS;

  //init the HAL library
  unsigned mNumSensors = 0;
  HAL_CALL_ERROR_EXIT(ilmsens_hal_initHAL(), "Error initialising the HAL library.");

  //save number of sensors returned by an successful initHAL()
  mNumSensors = (unsigned)mHalResult;

  //set HAL log level
  HAL_CALL_ERROR_EXIT(ilmsens_hal_setDEBLevel(sLogLevel), "Error setting the log level.");
  
  //get HAL version
  ilmsens_hal_Version tHALVersion;
  HAL_CALL_ERROR_EXIT(ilmsens_hal_getVersion(&tHALVersion), "Error reading the HAL library version.");

  //show version
  std::cout << "HAL library version is V" << std::dec << tHALVersion.mMajor << "." << tHALVersion.mMinor << "." << tHALVersion.mBuild << "." << std::endl;

  //show how many sensors have been detected.
  std::cout << "HAL library detected " << std::dec << mNumSensors << " sensors." << std::endl;
  if (mNumSensors == 0)
  {
    //nothing to do
    std::cout << "No sensors available, nothing to do." << std::endl;

    //cleanup, deinit the HAL
    ilmsens_hal_deinitHAL();
    return(0);
  }  

  //check selected sensor number
  if (sSenNum > mNumSensors)
  {
    std::cerr << "Error: selected sensor number " << std::dec << sSenNum 
              << " is out of range [0 .. " << std::dec << mNumSensors << "] (0 = only show IDs)!" << std::endl;

    //don't forget the deinit!
    ilmsens_hal_deinitHAL();
    return(1);
  }

  ////////////////////////////////////////////////////////////////////////
  // get device ID of all sensors
  ////////////////////////////////////////////////////////////////////////
	
  //create list of sensor order numbers: 1 ..  mNumSensors
  TSensorNumbers mSensorList;
  
  mSensorList.clear();
  for (unsigned tS = 0; tS < mNumSensors; ++tS)
  {
    mSensorList.push_back(tS+1);
  }
  
  //open the devices
  HAL_CALL_ERROR_EXIT(ilmsens_hal_openSensors (&mSensorList.front(), static_cast<unsigned>(mSensorList.size())), "Error opening the sensors.");

  //read out device IDs
  char tID[ILMSENS_HAL_MOD_ID_BUF_SIZE]; //max length allocated
  for(unsigned int tS=0; tS < mSensorList.size(); ++tS)
  {
    mHalResult = ilmsens_hal_getModId (mSensorList.at(tS), tID, sizeof(tID));
    
    std::cout << "Sensor #" << std::dec << mSensorList.at(tS) << " has ID '" << tID
              <<   "' (result was " << std::dec << mHalResult << ")." << std::endl;
  }
  
  //We are about to use only one of the sensors for a measurement.
  //The selected device must be master. If the user runs the application
  //multiple times and selects different sensors, we must make sure that there 
  //is only one master at any time. Therefore, set all sensors are to be slaves anyways.
  HAL_CALL_ERROR_EXIT(ilmsens_hal_setMaster (&mSensorList.front(), static_cast<unsigned>(mSensorList.size()), ILMSENS_HAL_SLAVE_SENSOR), "Error setting the sensors to slave mode.");

  //close the devices, only one will be used later
  ilmsens_hal_closeSensors (&mSensorList.front(), static_cast<unsigned>(mSensorList.size()));
  

  ////////////////////////////////////////////////////////////////////////
  // start a measuremement with the selected sensor
  ////////////////////////////////////////////////////////////////////////
  
  //remember errors during measurements
  unsigned mErrCnt = 0;
  
  //check selection number
  if (sSenNum == 0)
  {
    //user just wanted to see the IDs
    std::cout << "No sensor selected for measurement, nothing more to do." << std::endl;
  }
  else
  {
    //get sensor number
    unsigned tSenNum = mSensorList.at(sSenNum-1);
    
    //open the device
    HAL_CALL_ERROR_EXIT(ilmsens_hal_openSensors (&tSenNum, 1), "Error opening the sensor.");
    
    //setup sensor parameters
    ilmsens_hal_ModConfig tSenConfig;

    tSenConfig.mClk   = sMasterClk;     // RF system clock [GHz]
    tSenConfig.mOrder = sMLBSOrder;     // order of MLBS: 9, 12, or 15
    tSenConfig.mSub   = 0;              // clock divider for real sampling rate: 0 = use default
    tSenConfig.mOV    = 0;              // number of oversampling: 0 = use default
    tSenConfig.mTx    = 0;              // number of transmitters: 0 = use default
    tSenConfig.mRx    = sNumRx;         // number of Rx: usually 2 per sensor

    HAL_CALL_ERROR_EXIT(ilmsens_hal_setupSensors (&tSenNum, 1, &tSenConfig), "Error during basic setup of the sensor.");

    //set the sensor to master mode
    HAL_CALL_ERROR_EXIT(ilmsens_hal_setMaster (&tSenNum, 1, ILMSENS_HAL_MASTER_SENSOR), "Error setting the sensor to be master.");

    //perform digital synchronisation (set to off (sensor may have been synch'ed before), then to on again)
    HAL_CALL_ERROR_EXIT(ilmsens_hal_synchMS (&tSenNum, 1, ILMSENS_HAL_SYNCH_OFF), "Error unsynching the sensor.");
    HAL_CALL_ERROR_EXIT(ilmsens_hal_synchMS (&tSenNum, 1, ILMSENS_HAL_SYNCH_ON), "Error synching the sensor.");

    //start the transmitter after synchronisation
    HAL_CALL_ERROR_EXIT(ilmsens_hal_setMLBS (&tSenNum, 1), "Error starting the transmitter of the sensor.");

    //set the software averages and wait cycles
    HAL_CALL_ERROR_EXIT(ilmsens_hal_setAvg (&tSenNum, 1, sSWAvg, WAIT_CYC_DEFAULT), "Error setting up software averages and wait cycles.");
    
    //get & show the sensor's complete configuration
    ilmsens_hal_ModInfo tSenInfo;
    HAL_CALL_ERROR_EXIT(ilmsens_hal_getModInfo (tSenNum, &tSenInfo), "Error reading info of the sensor.");

    std::cout << "Configuration of selected sensor is :" << std::endl; 
    std::cout << "* RF system clock    [GHz]: " << std::dec << std::setprecision(6) << tSenInfo.mConfig.mClk << std::endl;
    std::cout << "* MLBS order              : " << std::dec << tSenInfo.mConfig.mOrder << std::endl;
    std::cout << "* Prescaler           1/  : " << std::dec << tSenInfo.mConfig.mSub << std::endl;
    std::cout << "* Oversampling        x   : " << std::dec << tSenInfo.mConfig.mOV << std::endl;
    std::cout << "* Number of Tx            : " << std::dec << tSenInfo.mConfig.mTx << std::endl;
    std::cout << "* Number of Rx            : " << std::dec << tSenInfo.mConfig.mRx << std::endl;
    std::cout << "* Number of samples per Rx: " << std::dec << tSenInfo.mNumSamp << std::endl;
    std::cout << "* Hardware averages       : " << std::dec << tSenInfo.mHWAvg << std::endl;
    std::cout << "* Software avg. limits    : [" << std::dec << tSenInfo.mAvgLim[0] << " .. " << tSenInfo.mAvgLim[1] << "]" << std::endl;
    std::cout << "* Software averages       : " << std::dec << tSenInfo.mAvg << std::endl;
    std::cout << "* Wait cycle limits       : [" << std::dec << tSenInfo.mWaitLim[0] << " .. " << tSenInfo.mWaitLim[1] << "]" << std::endl;
    std::cout << "* Wait cycles             : " << std::dec << tSenInfo.mWait << std::endl;
    std::cout << "* ADC full scale range [V]: [" << std::dec << std::setprecision(6) << tSenInfo.mFSR[0] << " .. " << tSenInfo.mFSR[1] << "]" << std::endl;
    std::cout << "* ADC LSB voltage     [mV]: " << std::dec << std::setprecision(6) << tSenInfo.mLSB_Volt*1000.0 << std::endl;
    std::cout << "* Int. temperature    [" << '\370' << "C]: " << std::dec << std::setprecision(2) << tSenInfo.mTemp << std::endl;

    //calculate the required buffer size for measured data
    // > number of measured samples per Rx is mNumSamp (which is (2^mOrder-1) * mOV)
    // > number of additional info per Rx is mOV
    // > total samples per Rx is mNumSamp + mOV
    unsigned tRxSize  = tSenInfo.mNumSamp + tSenInfo.mConfig.mOV;
    // - number of sensors is 1
    // - number of Rx of the sensor(s) is mRx
    unsigned tBufSize = 1 * tRxSize * tSenInfo.mConfig.mRx;

    //set the transmitter's power down feature
    HAL_CALL_ERROR_EXIT(ilmsens_hal_setPD (&tSenNum, 1, ILMSENS_HAL_TX_ON), "Error switching on the transmitter.");

    //do repeated measurements
    for (unsigned tRepMeas = 0; tRepMeas < sRepCnt; ++tRepMeas) 
    {
      std::cout << std::endl << "--- Starting test run #" << std::dec << (tRepMeas+1) << " ---" << std::endl;

      //start a buffered measurement
      HAL_CALL_ERROR_EXIT(ilmsens_hal_measRun (&tSenNum, 1, ILMSENS_HAL_RUN_BUF), "Error starting the measurement.");

      //create buffer for measured data
      TSampleBuffer tMeasBuffer;
      tMeasBuffer.resize(tBufSize); //resize fills with default values


      //retrieve data and mind the timeout
      auto tStartTime = high_resolution_clock::now();
      int tSequenceNumber = 0;
      for (unsigned tI = 0; tI < sIRFCnt; ++tI) 
      {
        //get next IRF
        HAL_CALL_ERROR_EXIT(ilmsens_hal_measGet (&tSenNum, 1, &tMeasBuffer.front(), static_cast<size_t>(tMeasBuffer.size() * sizeof(ilmsens_hal_SampleType)), sTOMillis), "Error reading measured data #" << std::dec << tI);
        
        //check returned size
        if ((unsigned)mHalResult != tBufSize) 
        {
          //display an error
          std::cerr << "Size of the dataset #" << std::dec << tI
            << " is " << std::dec << mHalResult << " sample(s) long,"
            << " but expected " << std::dec << tBufSize << " samples."
            << std::endl;

          //count the error
          ++mErrCnt;
        }
        else
        {
          //check sequence number: it is the frist additional info after the samples of Rx 1
          auto tCurSeqNum = tMeasBuffer[tSenInfo.mNumSamp];
          if (tCurSeqNum != tSequenceNumber++) 
          {
            //sequence number incorrect
            std::cerr << "Sequence number of the impulse-response #" << std::dec << tI
              << " is " << std::dec << tCurSeqNum << ","
              << " but expected " << std::dec << tSequenceNumber << ". Some data seems to be missing!"
              << std::endl;
            
            //set current sequence number as new one
            tSequenceNumber = tCurSeqNum;

            //count the error
            ++mErrCnt;
          }
          else
          {
            //show how much has already been received
            auto tDuration_ms = duration_cast<milliseconds>(high_resolution_clock::now() - tStartTime).count();
            std::cout << "Received impulse response #" << std::dec << tI << " with sequence number "
              << std::dec << tCurSeqNum << " after "
              << std::dec << tDuration_ms << " ms."
              << std::endl;

            //process the data
            auto tProcStartTime = high_resolution_clock::now();
            processMLBSData(tSenInfo, 1, tMeasBuffer);
            auto tProcDuration_ms = duration_cast<milliseconds>(high_resolution_clock::now() - tProcStartTime).count();
            std::cout << "Processing of impulse response #" << std::dec << tI << " took "
              << std::dec << tProcDuration_ms << " ms."
              << std::endl;
          }
        }
      }
      
      //report duration of current run
      auto tDuration_ms = duration_cast<milliseconds>(high_resolution_clock::now() - tStartTime).count();
      std::cout << "Read " << std::dec << sIRFCnt << " impulse responses from the sensor in "
        << std::dec << tDuration_ms / 1000.0 << " seconds."
        << std::endl;

      //stop the buffered measurement
      HAL_CALL_ERROR_EXIT(ilmsens_hal_measStop (&tSenNum, 1), "Error stopping the measurement.");
    }

    //close the sensor
    ilmsens_hal_closeSensors (&tSenNum, 1);
  }

  //cleanup, deinit the HAL
  ilmsens_hal_deinitHAL();
  
  return( mErrCnt == 0 ? 0 : 2);
}
