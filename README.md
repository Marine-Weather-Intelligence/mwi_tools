# Marine Weather Intelligence dev tools

### To install or get the latest release it just type : <br/>
```
pip install git+https://github.com/hokuleadev/mwi_tools.git
```


### To use packages : 
```
from mwi_tools import wind
from mwi_tools.polaire import *
from mwi_tools.polaire import polaire
from mwi_tools.grib import extract_grib 
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
 │   └── wind.py
 └── setup.py
```

 ### Some documentation

[Documentation](https://hokuleadev.github.io/mwi_tools/mwi_tools/index.html)

### To update package 

- Clone the directory <br>
  ```git clone https://github.com/hokuleadev/mwi_tools.git```
- Add your modules / submodules 
- Update the structure in readme file
- Update documentation by using this command in the mwi_tools repository <br>
  ```pdoc --output-dir ./docs --html mwi_tools -f```
- Update VERSION file
- Update requirements.txt if needed
- ```git add . ```
- ```git commit -m "update"```
- ```git push```
- ```pip install git+https://github.com/hokuleadev/mwi_tools.git```




