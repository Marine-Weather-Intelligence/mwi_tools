# Marine Weather Intelligence dev tools

To install or get the latest release it just type : 
pip install git+https://github.com/hokuleadev/mwi_tools.git


To use packages : 
from mwi_tools import wind
from mwi_tools.polaire import *
from mwi_tools.polaire import polaire
from mwi_tools.grib import extract_grib 


## Structure 

mwi_tools/<br>
 ├── LICENSE<br>
 ├── README.md<br>
 ├── VERSION<br>
 ├── requirements.txt<br>
 ├── mwi_tools/<br>
 │   ├── __init__.py<br>
 │   ├── coordinates<br>
 │   │   ├── __init__.py<br>
 │   │   ├── calculate.py<br>
 │   │   └── format.py<br>
 │   ├── datetime/<br>
 │   │   ├── __init__.py<br>
 │   │   ├── calculate.py<br>
 │   │   └── format.py<br>
 │   ├── grib/<br>
 │   │   ├── __init__.py<br>
 │   │   ├── extract.py<br>
 │   │   └── split.py<br>
 │   ├── polaire/<br>
 │   │   ├── __init__.py<br>
 │   │   └── polaire.py<br>
 │   ├── divers.py<br>
 │   ├── cloud.py<br>
 │   └── wind.py<br>
 └── setup.py<br>


 ## Some documentation

To see [documentation](https://hokuleadev.github.io/mwi_tools/mwi_tools/index.html) : 

## To update package 

- git clone the directory
- Add your modules / submodules 
- Update the structure in readme file
- Update documentation by using this command in the mwi_tools repository
            pdoc --output-dir ./docs --html mwi_tools -f
- Update VERSION file
- Update requirements if needed
- git add . 
- git commit -m "update"
- git push
- pip install git+https://github.com/hokuleadev/mwi_tools.git




