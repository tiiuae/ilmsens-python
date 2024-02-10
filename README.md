# ilmsens-python
 A python library to control the SH-3100 M9, M12 and M15 devices from ILMSENS.

<img src="https://image.jimcdn.com/app/cms/image/transf/dimension=640x10000:format=jpg/path/sd944a4ec3516c75a/image/if2715ced80e2c587/version/1584959803/ilmsens-technology-impedance-spectroscopy-network-analysis-time-domain-reflectometry-short-range-radar-microwave-imaging.jpg" width=100%>

### Table of Contents
**[Requirements](#requirements)**<br>
**[Installation Steps](#installation-steps)**<br>
**[Usage](#usage)**<br>
**[Documentation](#documentation)**<br>


- - - -

## Requirements
```
python>=3.6
numpy>=1.26.2
```
Tested on Ubuntu 18.04 and 16.04.

## Installation Steps
1. Download the HAL DEB-package to your computer (provided with the ilmsens device). Make sure to get the package matching your Linux distribution and architecture.
2. In the terminal, update your package index (optional) then install the `libusb-1.0-0-dev` and `libpoco-dev` dependencies.
   ```
   $ sudo apt update
   $ sudo apt install libusb-1.0-0-dev
   $ sudo apt install libpoco-dev
   ```
3. Install the downloaded DEB-package, using `dpkg` and the path to the downloaded DEB file.
   ```
   $ sudo dpkg -i ilmsens-hal-X.Y.Z-<dist_name><dist_ver>_<arch>.deb
   ```
   To test your HAL installation, go your binaries directory and run the `hal_itest` script.
   ```
   $ cd /usr/bin
   $ hal_itest --timeoutMillis 100 --responseCount 10 --logLevel trace 2> hal_itest.log
   ```
5. Install this package in your Python environment using the below command
   ```
   $ pip install git+https://github.com/tiiuae/ilmsens-python.git
   ```
For more information on steps 1 through 3, refer to the manufacturer's setup guide (See [Setup Guide](/manuals/Ilmsens_HAL_API_setup_guide.pdf)). They are the same steps.

## Usage
```python
import ilmsens_hal
import ilmsens_hal.utils

num_devices = ilmsens_hal.initHAL()
print(f"Found {num_devices} connected devices")

ver = ilmsens_hal.getVersion()
print(f"{ver.mMajor}.{ver.mMinor}.{ver.mBuild}")

device_index = 1
device_id = ilmsens_hal.getModId(device_index)
print(f"Sensor #{device_index} has ID '{device_id.decode()}' (result was {len(device_id)}).")
```
A complete example can be found included in the manuals directory (See [python_example.ipynb](/manuals/python_example.ipynb)).

## Documentation
The documentation for the Python module will be completed soon.
Meanwhile, the manufacturer's [Function Reference](/manuals/Ilmsens_HAL_API_Function_Reference.pdf) and [Programming Guide](/manuals/Ilmsens_HAL_API_programming_guide.pdf) can be used as the next closest reference.
