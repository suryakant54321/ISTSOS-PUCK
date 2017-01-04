# -*- coding: utf-8 -*-
"""
# istSOS WebAdmin - Istituto Scienze della Terra
# Copyright (C) 2012 Massimiliano Cannata, Milan Antonovic
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
#----------------------------------------------------------------------------------
# Modified by: Suryakant Sawant 
# Date: 03 Jan. 2016
# Objective: REST based approach to configure SenseTube service
# Command line interface to create sensor configurations in ISTSOS
#
# Operations covered in this script
# 1. Insert observations
#
# Envisaged application/ motivation
# 1. to facilitate PUCK implementation
#
# TODO:
# Add example to demonstrate sensor sampling and insert operation.
"""
#!/bin/python
import os#no need for finding files
import json
import pprint
import glob#no need for finding files
import requests as req
#
def insertObs(url, service, procs, lines):
	"""
	Function to insert observations in ISTSOS service.

	Input/s:
		url [str] service url (e.g. http://localhost/istsos)
		service [str] service name (e.g. test)
		procs [list] list of procedures (e.g. ['temp_1', 'temp_2'])

		lines [list] lines from file / observed property and observations
			first line should always be obseved properties for selected procedure.
			(e.g. 'urn:ogc:def:parameter:x-istsos:1.0:time:iso8601,
				urn:ogc:def:parameter:x-ksos:1.0:base:station2:village2:adc0,
				urn:ogc:def:parameter:x-ksos:1.0:base:station2:village2:air_temperature')

	Output/s:
		Success or failure messages

	TODO:
		Implement authentication.
	NOTE:
		Timestamp is strictly iso8601 (i.e. 2016-11-10T07:23:03.253207+05:30)
		e.g. now = datetime.datetime.now()
		     now = now.isoformat()+"+05:30" 
	"""
	pp = pprint.PrettyPrinter(indent=2)
	try:
		# Initializing URLs
		#url = args['u']
		# Procedures
		#service = args['s']
		# Quality index
		quality = '100'
		# Service instance name
		#procs = args['p']
		# Working directory, where the CSV files are located
		#wd = args['wd']
		# File extension
		#ext = args['e']
		debug = 'v'
		debug = ''
		test = ''#add some value if not test
		#user = args['usr']
		#passw = args['pwd']
		#req = requests.session()
		for proc in procs:
			print "Procedure: %s" % proc
			# Load procedure description
			print "GET: %s/wa/istsos/services/%s/procedures/%s" % (url,service,proc)
			res = req.get("%s/wa/istsos/services/%s/procedures/%s" % (url, service, proc), verify=False)
			data = res.json()
			if debug:
				pp.pprint(data)
			if data['success']==False:
				raise Exception ("Description of procedure %s can not be loaded: %s" % (proc, data['message']))
			else:
				if debug:
					pp.pprint(data)
				else:
					print " > %s" % data['message']
			data = data['data']
			aid = data['assignedSensorId']
			# Getting observed properties from describeSensor response
			op = []
			for out in data['outputs']:
				op.append(out['definition'])
			# Load of a getobservation request
			print "GET: %s/wa/istsos/services/%s/operations/getobservation/offerings/%s/procedures/%s/observedproperties/%s/eventtime/last" % (url,service,'temporary',proc,','.join(op))
			res = req.get("%s/wa/istsos/services/%s/operations/getobservation/offerings/%s/procedures/%s/observedproperties/%s/eventtime/last" % (url,service,'temporary',proc,','.join(op)), verify=False)
			data = res.json()
			if data['success']==False:
				raise Exception ("Last observation of procedure %s can not be loaded: %s" % (proc, data['message']))
			else:
				if debug:
					pp.pprint(data)
				else:
					print " > %s" % data['message']
			data = data['data'][0]
			data['AssignedSensorId'] = aid
			# Set values array empty (can contain 1 value if procedure not empty)
			data['result']['DataArray']['values'] = []
			# discover json observed property disposition
			jsonindex = {}
			for pos in range(0, len(data['result']['DataArray']['field'])):
				field = data['result']['DataArray']['field'][pos]
				jsonindex[field['definition']] = pos
			if debug:
				print "\njsonindex:"
				pp.pprint(jsonindex)
			#------------------------------------------------------------ 
			# skip searching files
			# find files
			#print "Searching: %s" % os.path.join(wd, "%s%s" % (proc,ext))
			#files = glob.glob(os.path.join(wd, "%s%s" % (proc,ext)))
			#print " > %s %s found" % (len(files), "Files" if len(files)>1 else "File")
			#for f in files:
			#	# open file
			#	file = open(f, 'rU')
			#	# loop lines
			#	lines = file.readlines()
			#------------------------------------------------------------
			obsindex = lines[0].strip(' \t\n\r').split(",")
			# Check if all the observedProperties of the procedure are included in the CSV file (quality index is optional)
			for k, v in jsonindex.iteritems():
				if k in obsindex:
					continue
				elif ':qualityIndex' in k:
					continue
				else:
					raise Exception ("Mandatory observed property %s is not present in the CSV." % k)
			begin = None
			end = None
			# loop lines skipping the header
			for i in range(1, len(lines)):
				try:
					line = lines[i]
					lineArray = line.strip(' \t\n\r').split(",")
					# Creating an empty array where the values will be inserted
					observation =  ['']*len(jsonindex)
					for k, v in jsonindex.iteritems():
						val = None
						if k in obsindex:
							val = lineArray[obsindex.index(k)]
						elif ':qualityIndex' in k: # Quality index is not present in the CSV so the default value will be set
							val = 	quality
						observation[v] = val
					# get first date
					if i == 1:
						begin = observation[jsonindex['urn:ogc:def:parameter:x-istsos:1.0:time:iso8601']]
					# get last date
					if i == (len(lines)-1):
						end   = observation[jsonindex['urn:ogc:def:parameter:x-istsos:1.0:time:iso8601']]
					# attach to object
					data['result']['DataArray']['values'].append(observation)
				except Exception as e:
					print "Everything was fine, I don't know what happned: %s" % i
					raise e
			data["samplingTime"] = {"beginPosition": begin, "endPosition": end};
			print "Begin: %s" % begin
			print "End: %s" % end
			print "Values: %s" % len( data['result']['DataArray']['values'])
			if debug:
				pp.pprint({"ForceInsert": "true","AssignedSensorId": aid, "Observation": data})
			# send to wa
			if not test:
				#print(aid)
				#print(data)
				aa = {"ForceInsert": "true", "AssignedSensorId": aid, "Observation": data}
				#user="postgres"
				#passw="postgres"
				#print(data)
				res = req.post("%s/wa/istsos/services/%s/operations/insertobservation" % (url, service), verify=False, data=json.dumps(aa))
			# read response
			if debug:
				pp.pprint(res.json())
			else:
				res = res.json()
				print " > Insert observation success: %s" % res['success']
				#print (res)
		pass
	except Exception as e:    
		print "ERROR: %s\n\n" % e
		#traceback.print_exc()
		pass
	pass
#---------------------
# Implementation
url = "http://localhost/istsos"
service = "test"
procs = ["temp_2"]#temp_2
# set path to data file
#f = "temp_2.DAT"
#file = open(f, 'rU')
#lines = file.readlines()
#insertObs(url, service, procs, lines)
