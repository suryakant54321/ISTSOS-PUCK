#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
#-----------------------------------------------------------------------
# Author: Suryakant Sawant
#
# Date: 25 Nov. 2016
#
# Objective: REST based approach to configure SenseTube service.
# Command line interface to parse SensorML and create SOS service instances in ISTSOS
#
# Operations covered
# 1. Read existing SensorML
# 2. Create observed properties
# 3. Create procedures
#
# Envisaged application/ motivation
# 1. to facilitate PUCK implementation
#
# TODO
# 1. Write plain text based parser to create service in ISTSOS
#-----------------------------------------------------------------------
"""
import xmltodict
import requests as req
import json
import re
#-----------------------------------------------------------------------
# 1. Create service
def createService(service):
	"""
	Function to create service in SOS database
	
	Input/s:
		Send service dict object as below  
		service = {"service": "test"}
	 
	Output/s:
		Returns response of http REST request
	"""
	address = 'http://localhost/istsos/wa/istsos/services'
	res = req.post(address, data=json.dumps(service))
	return(res)
#
# 2. Configure UOM's
def configUOM(url, uomDict):
	"""
	Function to create UOM in selected SOS 
	
	Input/s:
		url = 'http://localhost/istsos/wa/istsos/services/test/uoms'
		uomDict = {"name":"raw", "description":"Raw 10 bit ADC observation", "ForceInsert": "true"}
	
	Oputput/s:
		Returns response of http REST request
	"""
	res = req.post(url, data=json.dumps(uomDict))
	return(res)
#
# 3. Configure observed property using SensorML instances
def configObsProp(url, obsPropDict):
	"""
	Function to create Observed Properties in SOS
	
	Input/s:
		url = 'http://localhost/istsos/wa/istsos/services/krishisos/observedproperties'
		obsPropDict = {"definition": "urn:ogc:def:parameter:x-ksos:1.0:base:station1:village1:air_temperature", "constraint": [], "name": "air_temperature", "description": "temperature sensor at base station", "ForceInsert": "true"}

	Output/s:
		Returns response of http REST request
	"""
	res = req.post(url, data=json.dumps(obsPropDict))
	return(res)
#
# 4. Configure procedure using SensorML instances
def configProc(url, procDict):
	"""
	Function to create Procedures in SOS
	
	Input/s: 
		url = 'http://localhost/istsos/wa/istsos/services/test/procedures'
		procDict object with procedure details

	Output/s:
		Returns response of http REST request
	"""
	res = req.post(url, data=json.dumps(procDict))
	return(res)
#-----------------------------------------------------------------------
# Implementation
# Completed 1 & 2
# 1. Create Service
# 2. Configure UOM's
#
"""
#
url = 'http://localhost/istsos/wa/istsos/services/krishisosfour/uoms'
# 2. To inset UOM use post
resp1 = req.post(url, data=json.dumps({"name":"raw", "description":"Raw 10 bit ADC observation", "ForceInsert": "true"}) )
# Print output
print(resp1.status_code, resp1.text)
#
resp1 = req.post(url, data=json.dumps({"name":"celsius", "description":"Temperature sensor observation", "ForceInsert": "true"}) )
# Print output
print(resp1.status_code, resp1.text)
#
resp1 = req.post(url, data=json.dumps({"name":"percent", "description":"Percentage Relative Humidity or soil moisture", "ForceInsert": "true"}) )
# Print output
print(resp1.status_code, resp1.text)
"""
# Read SensorML (XML) 
# temp_1, temp_2, hum_bs_1, hum_bs_2, soil_moist_1, soil_moist_2, soil_temp_1, soil_temp_2
f = open("/location of ISTSOS-PUCK/data/temp_1.xml")
sml = f.readlines()
f.close()
# convert xml to dict object
sml = xmltodict.parse(sml[1])
#
# 3. Create Observed Properties
"""
# Sample 
obsPropDict = {"definition": "urn:ogc:def:parameter:x-ksos:1.0:base:station1:village1:air_temperature",\
		"constraint": [],\
		"name": "air_temperature",\
		"description": "temperature sensor at base station",\
		"ForceInsert": "true"}
"""
obsPropDict = {"definition": "urn:ogc:def:parameter:x-ksos:1.0:base:station1:village1:air_temperature", "constraint": [], "name": "air_temperature", "description": "temperature sensor at base station", "ForceInsert": "true"}
#
# Note changing service name
url = 'http://localhost/istsos/wa/istsos/services/test/observedproperties'
#
dd = sml['sml:SensorML']['sml:member']['sml:System']['sml:outputs']['sml:OutputList']['sml:output']['swe:DataRecord']['swe:field']
for i in range(0,len(dd)):
	if i != 0:
		obsPropDict['definition'] = dd[i]['swe:Quantity']['@definition']# adding definition
		obsPropDict['name'] = dd[i]['@name']# adding name
		obsPropDict['description'] = ""
		out = configObsProp(url, obsPropDict)
		print(out.status_code, out.text)
		print(obsPropDict)
#
# 4. create procedure
"""
# Sample procedure dict object
"""
procDict = {'capabilities': [],
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
                {'properties': {'name': '4326'}, 'type': '4326'},
            'geometry':{'coordinates': ["78.151889","21.449054","500"], 'type': 'Point'},
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
#
# Note: start from sml['sml:SensorML']['sml:member']['sml:System']
# Description
procDict['description'] = sml['sml:SensorML']['sml:member']['sml:System']['gml:description']
# Classification
# System Type
procDict['classification'][0]['value'] = sml['sml:SensorML']['sml:member']['sml:System']['sml:classification']['sml:ClassifierList']['sml:classifier'][0]['sml:Term']['sml:value']
# Sensor Type
procDict['classification'][1]['value'] = sml['sml:SensorML']['sml:member']['sml:System']['sml:classification']['sml:ClassifierList']['sml:classifier'][0]['sml:Term']['sml:value']
# keywords for procedure
procDict['keywords'] = sml['sml:SensorML']['sml:member']['sml:System']['sml:keywords']['sml:KeywordList']['sml:keyword']
# System
procDict['system'] = sml['sml:SensorML']['sml:member']['sml:System']['gml:name']
# System ID
procDict['system_id'] = sml['sml:SensorML']['sml:member']['sml:System']['@gml:id']
# Location details
# procDict['location'] = 
procDict['location']['crs']['properties']['name'] = '4326'#sml['sml:SensorML']['sml:member']['sml:System']['sml:location']['gml:Point']['@srsName']
procDict['location']['crs']['type'] = '4326'# sml['sml:SensorML']['sml:member']['sml:System']['sml:location']['gml:Point']['@srsName']
# Split coordinates
co = re.split(',', sml['sml:SensorML']['sml:member']['sml:System']['sml:location']['gml:Point']['gml:coordinates'])
procDict['location']['geometry']['coordinates'][0] = str(co[0]) # Longitude
procDict['location']['geometry']['coordinates'][1] = str(co[1]) # Latitude
procDict['location']['geometry']['coordinates'][2] = str(co[2]) # Elevation
# Name
procDict['location']['properties']['name'] = sml['sml:SensorML']['sml:member']['sml:System']['sml:location']['gml:Point']['@gml:id']
# Outputs 
# procDict['outputs'][0] # TODO: Time stamp outputs not configured  
# Outputs Observed property and associated UOM
for i in range(0, len(procDict['outputs'])):
	if i != 0:
		procDict['outputs'][i]['name'] = sml['sml:SensorML']['sml:member']['sml:System']['sml:outputs']['sml:OutputList']['sml:output']['swe:DataRecord']['swe:field'][i]['@name']
		procDict['outputs'][i]['description'] = sml['sml:SensorML']['sml:member']['sml:System']['sml:outputs']['sml:OutputList']['sml:output']['swe:DataRecord']['swe:field'][i]['@name']
		procDict['outputs'][i]['definition'] = sml['sml:SensorML']['sml:member']['sml:System']['sml:outputs']['sml:OutputList']['sml:output']['swe:DataRecord']['swe:field'][i]['swe:Quantity']['@definition']
		procDict['outputs'][i]['uom'] = sml['sml:SensorML']['sml:member']['sml:System']['sml:outputs']['sml:OutputList']['sml:output']['swe:DataRecord']['swe:field'][i]['swe:Quantity']['swe:uom']['@code']
		# procDict['outputs'][i]['constraint'] # TODO: constraint not added
# Following are empty
# capabilities, contacts, documentation, identification, inputs, interfaces, history
#
# Note changing service name
url = 'http://localhost/istsos/wa/istsos/services/test/procedures'
print(procDict)
out = configProc(url, procDict)
print(out.status_code, out.text)

