# ISTSOS-PUCK
OGC PUCK (plug-n-play) implementation for ISTSOS in [SenseTube/KrishiSense] sensing system

- Python based ISTSOS (wa lib) based REST implementation.
- To facilitate OGC PUCK implementation mainly in [SenseTube/KrishiSense] sensing system

### Version
Alpha 0.1.0


### Depends on

It is assumed that ISTSOS 1.1.0 or 2.2.0 is already installed and running.

Only tested in Ubuntu 16.04 with python 2.7, ISTSOS 2.2.0, depends on following

- requests

### Contains

1. Folder: src
	- sosPUCKcreteService.py (Create service in ISTSOS using REST 'i.e. walib')
2. Folder: data
	- temp_1.DAT (Sample SenseTube data)

### Advantages

1. Facilitate Python based PUCK implementation for ISTSOS.

### Limitations

1. Need some understanding of OGC SOS and ISTSOS.
2. Long script may confuse.

### Other References

- [OGC] Open Geospatial Consortium
- OGC [SOS] Specifications
- Python based SOS [ISTSOS]
	
### Installation

A. Download

- Clone from GitHub

```sh
$ git clone https://github.com/suryakant54321/ISTSOS-PUCK 
```

- Install dependencies 

```sh
$ cd ISTSOS-PUCK
$ pip install -r requirements.txt 
```

B. Usage of ISTSOS-PUCK

	For now there is only one script "sosPUCKcreteService.py"
	Open script in text editor / directly execute using python / ipython

```sh
$ python sosPUCKcreteService.py
```

C. For SOS Clients 

To check the successful service configuration using ISTSOS-PUCK.

- Refer [Python-SOS-Client] Python based client for ISTSOS 
- Refer [PHP-istSOS-client] PHP based client for ISTSOS
- Refer [sos4R] sos4R is an extension for the R environment for statistical computing and visualization. Designed by [52°North].
- Refer [sos-js] a JavaScript library to browse, visualise, and access, data from an Open Geospatial Consortium (OGC) Sensor Observation Service (SOS). Designed by [52°North].


#### TODO

1. Write .xml parser to access details from existing SensorML
2. Write plain text based parser to configure ISTSOS service



[ISTSOS]: <http://istsos.org/>
[ISTSOS-Demo]: <http://istsos.org/istsos/demo?request=getCapabilities&section=contents&service=SOS>
[NDBC]: <http://sdf.ndbc.noaa.gov/sos/>
[NDBC-SOS]: <http://sdf.ndbc.noaa.gov/sos/server.php?request=GetCapabilities&service=SOS>
[OGC]: <http://www.opengeospatial.org/>
[SOS]: <http://www.opengeospatial.org/standards/sos>
[PHP-istSOS-client]: <https://github.com/suryakant54321/php_istSOS_client>
[sos4R]: <https://github.com/52North/sos4R>
[sos-js]: <https://github.com/52North/sos-js>
[52°North]: <http://52north.org/>
[Sphinix]: <http://www.sphinx-doc.org/en/stable/>
[Telegram Bot Platform]: <https://telegram.org/blog/bot-revolution>
[Telegram-Bot-Scripts]: <https://github.com/suryakant54321/Telegram-Bot-Scripts>
[python-telegram-bot]: <https://github.com/python-telegram-bot/python-telegram-bot>
[IWC project]: <http://itra.medialabasia.in/?p=623>
[Python-SOS-Client]: <https://github.com/suryakant54321/Python-SOS-Client>
[SenseTube/KrishiSense]: <http://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=6947385&isnumber=6946328>
