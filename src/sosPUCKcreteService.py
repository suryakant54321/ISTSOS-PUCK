#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
#-----------------------------------------------------------------------
# Author: Suryakant Sawant
#
# Date: Started by Mr. Pankaj Randhe sometime in Aug. 2015.
# Completed by Mr. Suryakant during 16 Sept. 2016 - 24 Nov. 2016
#
# Objective: REST based approach to configure SenseTube service
# Command line interface to create sensor configurations in ISTSOS
#
# Operations covered
# 1. Create service , Delete Service
# 2. Read service configurations
# 3. Configure UOM's (view, insert, delete)
# 4. Configure observed property
# 5. Configure procedure
# 6. Insert observations
#-----------------------------------------------------------------------
"""
import requests as req
import json
#-----------------------------------------------------------------------
# 1. Create service
service = {"service": "test"}
address = 'http://localhost/istsos/wa/istsos/services'
res = req.post(address, data=json.dumps(service))
# 2. delete service
deladdress = 'http://localhost/istsos/wa/istsos/services/test'
delres = req.delete(deladdress)
#-----------------------------------------------------------------------
# 2. Read service configurations 
url2 = 'http://localhost/istsos/wa/istsos/services/test/configsections'
resp = req.get(url2)
#
print(resp2.status_code, resp2.text)
#-----------------------------------------------------------------------
# 3. Configure UOM's
# 1. To read the UOM's use get request
url = 'http://localhost/istsos/wa/istsos/services/test/uoms'
resp2 = req.get(url)
# Print output
print(resp2.status_code, resp2.text)
#
# 2. To inset UOM use post
resp1 = req.post(url, data=json.dumps({"name":"raw", "description":"Raw 10 bit ADC observation", "ForceInsert": "true"}) )
# Print output
print(resp1.status_code, resp1.text)
#
resp1 = req.post(url, data=json.dumps({"name":"Celsius", "description":"Temperature sensor observation", "ForceInsert": "true"}) )
# Print output
print(resp1.status_code, resp1.text)
#
resp1 = req.post(url, data=json.dumps({"name":"percent", "description":"Percentage Relative Humidity or soil moisture", "ForceInsert": "true"}) )
# Print output
print(resp1.status_code, resp1.text)
#
resp1 = req.post(url, data=json.dumps({"name":"ppm", "description":"concentration of gas in parts per million", "ForceInsert": "true"}) )
# Print output
print(resp1.status_code, resp1.text)
#
# 3. To delete some UOM url should be pointed at that UOM
resp2 = req.delete(url+'/ppm', data=json.dumps({"name":"ppm", "description":"concentration of gas in parts per million", "ForceInsert": "true"}) )
# Print output
print(resp2.status_code, resp2.text)
#-----------------------------------------------------------------------
# 4. Configure observed property
# a) air_temperature
# urn:ogc:def:parameter:x-ksos:1.0:base:station1:village1:air_temperature
opr = {"definition": "urn:ogc:def:parameter:x-ksos:1.0:base:station1:village1:air_temperature", "constraint": [], "name": "air_temperature", "description": "temperature sensor at base station", "ForceInsert": "true"}
url = 'http://localhost/istsos/wa/istsos/services/test/observedproperties'
resp1 = req.post(url, data=json.dumps(opr) )
# Print output
print(resp1.status_code, resp1.text)
# b) adc
opr = {"definition": "urn:ogc:def:parameter:x-ksos:1.0:base:station1:village1:adc0", "constraint": [], "name": "raw_adc_0", "description": "10 bit ADC value", "ForceInsert": "true"}
url = 'http://localhost/istsos/wa/istsos/services/test/observedproperties'
resp1 = req.post(url, data=json.dumps(opr) )
# Print output
print(resp1.status_code, resp1.text)
#-----------------------------------------------------------------------
# 5. Configure procedure
#
tproc = {
        'capabilities': [],
        'characteristics': '',
        'classification': [
            {'definition': 'urn:ogc:def:classifier:x-istsos:1.0:systemType',
             'name': 'System Type',
             'value': 'insitu-fixed-point'},
            {'definition': 'urn:ogc:def:classifier:x-istsos:1.0:sensorType',
             'name': 'Sensor Type',
             'value': 'analog, based on tehermocouple'}],
        'contacts': [],
        'description': 'temperature sensor at base station',
        'documentation': [],
        'history': [],
        'identification': [],
        'inputs': [],
        'interfaces': '',
        'keywords': 'temperature',
        'location': 
            {'crs': 
                {'properties': 
                    {'name': '4326'}, 
                'type': '4326'},
            'geometry': 
                {'coordinates': ["78.151889","21.449054","500"], 
                'type': 'Point'},
            'properties': 
                {'name': 'temperature_sensor_1'},
            'type': 'Feature'},
         'outputs': [
             {
                'definition': 'urn:ogc:def:parameter:x-istsos:1.0:time:iso8601',
                'description': '',
                'name': 'Time',
                'uom': 'iso8601'
             },
            {
                 'constraint': {'min': '0', 'role': 'urn:ogc:def:classifiers:x-istsos:1.0:qualityIndex:check:reasonable'},
                 'definition': 'urn:ogc:def:parameter:x-ksos:1.0:base:station1:village1:air_temperature',
                 'description': 'air_temperature',
                 'name': 'air_temperature',
                 'uom': 'Celsius'
             },
            {
                 'constraint': {'min': '0', 'role': 'urn:ogc:def:classifiers:x-istsos:1.0:qualityIndex:check:reasonable'},
                 'definition': 'urn:ogc:def:parameter:x-ksos:1.0:base:station1:village1:adc0',
                 'description': 'raw_adc_0',
                 'name': 'raw_adc_0',
                 'uom': 'raw'
             }
         ],
         'system': 'temp_1',
         'system_id': 'temp_1'}
address = 'http://localhost/istsos/wa/istsos/services/test/procedures'
resp1 = req.post(address, data=json.dumps(tproc))
# Print output
print(resp1.status_code, resp1.text)
#-----------------------------------------------------------------------
# 6. Insert observations
# Note:	Convert CSV file into .DAT
# 	cmdimportcsv.py from istsos version 1.1 is used
cd /usr/local/istsos
#
python cmdimportcsv.py -p temp_1 -s test -u http://localhost/istsos -w "/path to ISTSOS-PUCK download directory/data/"
#-----------------------------------------------------------------------

