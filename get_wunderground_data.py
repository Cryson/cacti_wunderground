#!/usr/bin/python
#
# Get weather data from weather underground
# to graph into cacti
#
# Author: Cryson
# Date: 12/12/2016
#

import os
import urllib2, json, pprint, sys
from pprint import pprint
import datetime
import time

###### \/\/\/\/\/\/\/\/\/\/\/\/\/\/\ ######
###### FILL OUT YOUR VARIABLES BELOW ######
###### \/\/\/\/\/\/\/\/\/\/\/\/\/\/\ ######

#APIID/Key from weatherunderground
user_apiid=""

#City, e.g. New_York
user_city=""

#State e.g. MN, FL, CA
user_state=""

#Where is your weather cache file going to be located?
#Example: /opt/usertest/test/weather.data
cachefile=""


def getWeatherCondition(city) :
	global jsondata
	try :
		url = "http://api.wunderground.com/api/"
		url += "%s/conditions/q/%s/" % (user_apiid, user_state)
		url += "%s.json" % city
		req = urllib2.Request(url)
		response = urllib2.urlopen(req)
		jsondata = response.read()
		return jsondata
	except Exception :
		print("Could not get weather data")
		return response.read()


def checkcache_mtime():
	global minutes
	epoch = os.path.getmtime(cachefile)
	currenttime = time.time()
	seconds = currenttime - epoch
	minutes = seconds // 60 % 60

def pull_weather_json():
	weather = getWeatherCondition(user_city)
	w = json.loads(weather)

	#Grab Weather Data from Json into variables
	name = w['current_observation']['display_location']['city']
	currenttemp = float(w['current_observation']['temp_f'])
	atmospressure = float(w['current_observation']['pressure_in'])
	windspeed = float(w['current_observation']['wind_mph'])
	winddir = w['current_observation']['wind_dir']
	timeepoch = float(w['current_observation']['local_epoch'])
	realtime = datetime.datetime.fromtimestamp(timeepoch).strftime('%c')
	humidity = w['current_observation']['relative_humidity']
	humidity = humidity[:-1]
	humidity = float(humidity)
	feels_like = float(w['current_observation']['feelslike_f'])
	dewpoint = float(w['current_observation']['dewpoint_f'])
	outsideweather = w['current_observation']['weather']

	#create cache file
	f = open(cachefile, 'w')
	f.write("DEW:%.2f CURRTEMP:%.2f FEELS:%.2f HUM:%.2f WINDSP:%.2f PRESS:%.2f" % (dewpoint, currenttemp, feels_like, humidity, windspeed, atmospressure))
	f.close()

	#print cache file
	f = open(cachefile, 'r')
	contents = f.read()
	print(contents)
	f.close()


#####MAIN
if os.path.exists(cachefile):
	checkcache_mtime()
	if minutes > 15:
		pull_weather_json()
	elif minutes < 15:
		f = open(cachefile, 'r')
		contents = f.read()
		print(contents)
		f.close()
else:
	pull_weather_json()
