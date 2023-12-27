import codecs
import os.path
from setuptools import setup

def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()

def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")

setup(
    name="ilmsens_hal",
    version=get_version("ilmsens_hal/__init__.py"),
    python_requires=">=3.6",
    packages=[
        "ilmsens_hal",
        "ilmsens_hal.utils",
    ],
    package_data={
        "ilmsens_hal.utils": [
            "mlbs9.txt",
            "mlbs12.txt",
            "mlbs15.txt"
        ]
    },
    dependencies = [

    ]
)
