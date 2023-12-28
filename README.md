# ilmsens-python
 A python library to control the SH-3100 M9 and M12 devices from ILMSENS.

<img src="https://image.jimcdn.com/app/cms/image/transf/dimension=640x10000:format=jpg/path/sd944a4ec3516c75a/image/if2715ced80e2c587/version/1584959803/ilmsens-technology-impedance-spectroscopy-network-analysis-time-domain-reflectometry-short-range-radar-microwave-imaging.jpg" width=100%>

### Table of Contents
**[Requirements](#requirements)**<br>
**[Installation Steps](#installation-steps)**<br>
**[Usage](#usage)**<br>


- - - -

## Requirements
```
python>=3.6
```
## Installation Steps
    $ pip install ilmsens-python

## Usage
```python
import ilmsens_hal
import ilmsens_hal.utils

num_devices = ilmsens_hal.initHAL()
print(f"Found {num_devices} connected devices")

ver = ilmsens_hal.getVersion()
print(f"{ver.mMajor}.{ver.mMinor}.{ver.mBuild}")
```

