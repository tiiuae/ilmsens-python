# ilmsens-python
 A python library to control the SH-3100 M9, M12 and M15 devices from ILMSENS.

<img src="https://image.jimcdn.com/app/cms/image/transf/dimension=640x10000:format=jpg/path/sd944a4ec3516c75a/image/if2715ced80e2c587/version/1584959803/ilmsens-technology-impedance-spectroscopy-network-analysis-time-domain-reflectometry-short-range-radar-microwave-imaging.jpg" width=100%>

### Table of Contents
**[Requirements](#requirements)**<br>
**[Installation Steps](#installation-steps)**<br>
**[Usage](#usage)**<br>


- - - -

## Requirements
```
python>=3.6
numpy>=1.26.2
```
## Installation Steps
1. Follow the steps in the manufacturer's setup guide (See [Ilmsens_HAL_API_setup_guide](/manuals/Ilmsens_HAL_API_setup_guide.pdf)).
2. Install this package in your Python environment using the below command
```
$ pip install git+https://github.com/tiiuae/ilmsens-python.git
```

## Usage
```python
import ilmsens_hal
import ilmsens_hal.utils

num_devices = ilmsens_hal.initHAL()
print(f"Found {num_devices} connected devices")

ver = ilmsens_hal.getVersion()
print(f"{ver.mMajor}.{ver.mMinor}.{ver.mBuild}")
```

