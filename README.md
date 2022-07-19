# Marine Weather Intelligence dev tools

### To install type : <br/>
```
pip install git+https://github.com/Marine-Weather-Intelligence/mwi_tools.git
```
### To upgrade to the latest release just type : <br/>
```
pip install git+https://github.com/Marine-Weather-Intelligence/mwi_tools.git --upgrade
```


### To use packages : 
```
from mwi_tools import wind
from mwi_tools.polaire import *
from mwi_tools.polaire import polaire
from mwi_tools.grib import extract
```

### Structure 

```
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
 │   ├── basile.py 
 │   ├── posreport.py
 │   └── wind.py
 └── setup.py
```

 ### Some documentation

[Documentation](https://marine-weather-intelligence.github.io/mwi_tools/)

### To update package 

- Clone the directory <br>
  ```git clone https://github.com/Marine-Weather-Intelligence/mwi_tools.git```
- Add your modules / submodules 
- Update the structure in readme file
- Update documentation by using this command in the mwi_tools repository <br>
  ```pdoc --output-dir ./docs --html mwi_tools -f```
- Update VERSION file
- Update requirements.txt if needed
- ```git add . ```
- ```git commit -m "update"```
- ```git push```
- ```pip install git+https://github.com/Marine-Weather-Intelligence/mwi_tools.git```




