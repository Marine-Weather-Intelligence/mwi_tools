# Marine Weather Intelligence dev tools


**Don't forget to change the version file and update this readme file if you're adding any function or subpackage to the existing one.**


To install or get the latest release it just type : 
pip install git+https://github.com/hokuleadev/mwi_tools.git


To use packages : 
from mwi_tools import wind
from mwi_tools.polaire import *
from mwi_tools.polaire import polaire
from mwi_tools.grib import extract_grib 


## Structure 

mwi_tools/
 ├── LICENSE
 ├── README.md
 ├── VERSION
 ├── requirements.txt
 ├── mwi_tools/
 │   ├── __init__.py
 │   ├── coordinates
 │   │   ├── __init__.py
 │   │   ├── calculate.py
 │   │   └── format.py
 │   ├── datetime/
 │   │   ├── __init__.py
 │   │   ├── calculate.py
 │   │   └── format.py
 │   ├── grib/
 │   │   ├── __init__.py
 │   │   ├── extract.py
 │   │   └── split.py
 │   ├── polaire/
 │   │   ├── __init__.py
 │   │   └── polaire.py
 │   ├── divers.py
 │   ├── cloud.py
 │   └── wind.py
 └── setup.py


 ## Some documentation
To update documentation : 
