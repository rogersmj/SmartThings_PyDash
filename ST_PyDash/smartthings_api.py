#! /usr/bin/python
#################################################
#			SmartThings Python API				#
#################################################
# Zachary Priddy - 2015 						#
# me@zpriddy.com 								#
#												#
# Features: 									#
#	- Read and Write capabilities with 			#
#		SmartThings	using RESTapi				#
#################################################
#################################################


#################################################
# TO DO:
# -Add Thermostat Control
# -Add HUE Intagration

import os
import sys
import requests
import pprint
import json
import math

base_auth_url = "https://graph.api.smartthings.com/oauth/authorize?response_type=code&client_id="
base_auth_url2 = "&scope=app&redirect_uri="

callback_auth_url = "https://graph.api.smartthings.com/oauth/token?grant_type=authorization_code&client_id=CLIENTID&client_secret=CLIENTSECRECT&redirect_uri=URL&scope=app&code=CODE"


icons = {
	'chanceflurries': '&#xe036',
	'chancerain': '&#xe009',
	'chancesleet': '&#xe003',
	'chancesnow': '&#xe036',
	'chancetstorms': '&#xe025',
	'clear': '&#xe028',
	'cloudy': '&#xe000',
	'flurries': '&#xe036',
	'fog': '&#xe01b',
	'hazy': '&#xe01b',
	'mostlycloudy': '&#xe001',
	'mostlysunny': '&#xe001',
	'partlycloudy': '&#xe001',
	'partlysunny': '&#xe001',
	'sleet': '&#xe003',
	'rain': '&#xe009',
	'snow': '&#xe036',
	'sunny': '&#xe028',
	'tstorms': '&#xe025'
}

class SmartThings(object):
	def __init__(self, apiFile="smartthings.json", authFile="oauthin.json"):
		global base_auth_url
		global base_auth_url2
		global callback_auth_url

		self.verbose = True
		self.apiSettings = {}
		self.endpointd = {}
		self.deviceds = {}
		self.authorized = False
		self.client_id = None
		self.authURL = None

		if(os.path.isfile(apiFile)):
			self.authorized = True
			load_settings()

		if(os.path.isfile(authFile)):
			with open(authfile) as oauthfile:
				oauthIn = json.load(oauthfile)
			self.client_id = oauthIn["client_id"]
			self.authURL = base_auth_url + oauthIn['client_id'] + base_auth_url2 + quote(url)	

	def isAuthorized():
		return self.authorized

	def authURL():
		return self.authURL

	def authorize(url,settingsFile="smartthings.json", filename="oauthin.json"):
		return self.authURL


	def reauth(url,settingsFile="smartthings.json", filename="oauthin.json"):
		global smartThings
		global allDevices
		global oauthIn

		oauthIn = {}
		with open(filename) as oauthfile:
			oauthIn = json.load(oauthfile)

		authURL = base_auth_url + oauthIn['client_id'] + base_auth_url2 + quote(url)	
		return authURL

	def authSecond(code, url, filename="smartthings.json"):
		global smartThings
		global allDevices
		global oauthIn

		authdata = {}

		authURL = callback_auth_url.replace("CLIENTID",oauthIn['client_id']).replace("CLIENTSECRECT",oauthIn['client_secret']).replace("CODE",code).replace("URL",quote(url))
		authdata = requests.get(authURL).json()
		authdata['client_id'] = oauthIn['client_id']
		authdata['client_secret'] = oauthIn['client_secret']
		authdata['api'] = "https://graph.api.smartthings.com/api/smartapps/endpoints/" + oauthIn['client_id'] + "/"
		authdata['api_location'] = "graph.api.smartthings.com"

		#print authdata

		with open(filename,'w') as oauthfile:
			json.dump(authdata,oauthfile)

		return "/init"


	def load_settings(self, filename="smartthings.json"):
		"""Load the JSON Settings file. 
		
		See the documentation, but briefly you can
		get it from here:
		https://iotdb.org/playground/oauthorize
		"""

		with open(filename) as fin:
			self.apiSettings = json.load(fin)

	def request_endpoints(self):
		"""Get the endpoints exposed by the SmartThings App
		
		The first command you need to call
		"""

		endpoints_url = self.apiSettings["api"]
		endpoints_paramd = {
			"access_token": self.apiSettings["access_token"]
		}

		endpoints_response = requests.get(url=endpoints_url, params=endpoints_paramd)
		self.endpointd = endpoints_response.json()[0]


	def request_devices(self, device_type, device_id=None):
		"""List the devices"""

		devices_url = "https://graph.api.smartthings.com%s/%s" % ( self.endpointd["url"], device_type )
		devices_paramd = {
			"deviceId":device_id,
		}
		devices_headerd = {
			"Authorization": "Bearer %s" % self.apiSettings["access_token"],
			"deviceId":device_id
		}

		devices_response = requests.get(url=devices_url, params=devices_paramd, headers=devices_headerd, json=devices_paramd)
		#print devices_response.headers
		self.deviceds = devices_response.json()



		return self.deviceds

	def command_devices(self, device_type, device_id, command):

		devices_url = "https://graph.api.smartthings.com%s/%s" % ( self.endpointd["url"], device_type )
		devices_paramd = {
			"deviceId":device_id,
			"mode":command
		}
		devices_headerd = {
			"Authorization": "Bearer %s" % self.apiSettings["access_token"],
			"deviceId":device_id
		}
		devices_response = requests.post(url=devices_url, params=devices_paramd, headers=devices_headerd, json=devices_paramd)
		self.deviceds = devices_response.json()

		return self.deviceds

	def command_switch(self, device_id, command):
		if(command == "t"):
			currentState = self.request_devices("switch", device_id)['switch']
			if(currentState == 'on'):
				command = 'off'
			else:
				command = 'on'

		devices_url = "https://graph.api.smartthings.com%s/%s" % ( self.endpointd["url"], "switch" )
		devices_paramd = {
			"deviceId":device_id,
			"command":command
		}
		devices_headerd = {
			"Authorization": "Bearer %s" % self.apiSettings["access_token"],
		}
		devices_response = requests.post(url=devices_url, params=devices_paramd, headers=devices_headerd, json=devices_paramd)
		self.deviceds = devices_response.json()

		return command

	def command_dimmer(self, device_id, command):
		if(command == "t"):
			self.deviceds = self.command_switch(device_id,"t")
		else:
			devices_url = "https://graph.api.smartthings.com%s/%s" % ( self.endpointd["url"], "dimmer" )
			devices_paramd = {
				"deviceId":device_id,
				"command": "setLevel"

			}
			devices_headerd = {
				"Authorization": "Bearer %s" % self.apiSettings["access_token"],
			}
			devices_response = requests.post(url=devices_url, params=devices_paramd, headers=devices_headerd, json=devices_paramd)

			devices_url = "https://graph.api.smartthings.com%s/%s" % ( self.endpointd["url"], "dimmerLevel" )
			devices_paramd = {
				"deviceId":device_id,
				"command": command

			}
			devices_headerd = {
				"Authorization": "Bearer %s" % self.apiSettings["access_token"],
			}
			devices_response = requests.post(url=devices_url, params=devices_paramd, headers=devices_headerd, json=devices_paramd)

			self.deviceds = devices_response.json()

		return self.deviceds

	def set_color(self,deviceId,color):
		devices_url = "https://graph.api.smartthings.com%s/%s" % ( self.endpointd["url"], "color" )
		devices_paramd = rgbToHsl(color)
		devices_paramd['deviceId'] = deviceId
		devices_headerd = {
			"Authorization": "Bearer %s" % self.apiSettings["access_token"],
		}

		devices_response = requests.post(url=devices_url, params=devices_paramd, headers=devices_headerd, json=devices_paramd)

		return self.deviceds

	def set_color_hsla(self,deviceId,hue,sat,color):
		devices_url = "https://graph.api.smartthings.com%s/%s" % ( self.endpointd["url"], "color" )
		devices_paramd = {}
		devices_paramd['hex'] = color
		devices_paramd['hue'] = hue
		devices_paramd['sat'] = sat
		devices_paramd['deviceId'] = deviceId
		devices_headerd = {
			"Authorization": "Bearer %s" % self.apiSettings["access_token"],
		}

		devices_response = requests.post(url=devices_url, params=devices_paramd, headers=devices_headerd, json=devices_paramd)

		return self.deviceds
		


	def command_mode(self, mode_id):
		devices_url = "https://graph.api.smartthings.com%s/%s" % ( self.endpointd["url"], "mode" )
		devices_paramd = {
			"mode":mode_id
		}
		devices_headerd = {
			"Authorization": "Bearer %s" % self.apiSettings["access_token"],
		}

		devices_response = requests.post(url=devices_url, params=devices_paramd, headers=devices_headerd, json=devices_paramd)
		devices_response = requests.post(url=devices_url, params=devices_paramd, headers=devices_headerd, json=devices_paramd)
		self.deviceds = devices_response.json()

		return self.deviceds

	def get_mode(self):
		devices_url = "https://graph.api.smartthings.com%s/%s" % ( self.endpointd["url"], "mode" )
		devices_paramd = {

		}
		devices_headerd = {
			"Authorization": "Bearer %s" % self.apiSettings["access_token"],
		}

		devices_response = requests.get(url=devices_url, params=devices_paramd, headers=devices_headerd, json=devices_paramd)
		self.deviceds = devices_response.json()
		return self.deviceds


	def get_weather(self):
		devices_url = "https://graph.api.smartthings.com%s/%s" % ( self.endpointd["url"], "weather" )
		devices_paramd = {
			
		}
		devices_headerd = {
			"Authorization": "Bearer %s" % self.apiSettings["access_token"],
		}

		devices_response = requests.get(url=devices_url, params=devices_paramd, headers=devices_headerd, json=devices_paramd)
		self.weather = devices_response.json()

		weatherInfo = {}
		weatherInfo['location'] = self.weather['current_observation']['display_location']['full']
		weatherInfo['sky'] = self.weather['current_observation']['weather']
		weatherInfo['wind'] = self.weather['current_observation']['wind_mph']
		weatherInfo['temperature'] = self.weather['current_observation']['temp_f']
		weatherInfo['humidity'] = self.weather['current_observation']['relative_humidity']

		devices_url = "https://graph.api.smartthings.com%s/%s" % ( self.endpointd["url"], "weather" )
		devices_paramd = {
			'feature': 'forecast'
			
		}
		devices_headerd = {
			"Authorization": "Bearer %s" % self.apiSettings["access_token"],
		}

		devices_response = requests.get(url=devices_url, params=devices_paramd, headers=devices_headerd, json=devices_paramd)
		self.weather = devices_response.json()

		weatherInfo['low'] = self.weather["forecast"]["simpleforecast"]["forecastday"][0]["low"]["fahrenheit"]
		weatherInfo['high'] = self.weather["forecast"]["simpleforecast"]["forecastday"][0]["high"]["fahrenheit"]
		weatherInfo['icon'] = icons[self.weather["forecast"]["simpleforecast"]["forecastday"][0]["icon"]]
		weatherInfo['precip'] =  self.weather["forecast"]["simpleforecast"]["forecastday"][0]["pop"]
		weatherInfo['tomorrow_temp_low'] =  self.weather["forecast"]["simpleforecast"]["forecastday"][1]["low"]["fahrenheit"]
		weatherInfo['tomorrow_temp_high'] =  self.weather["forecast"]["simpleforecast"]["forecastday"][1]["high"]["fahrenheit"]
		weatherInfo['tomorrow_icon'] =  icons[self.weather["forecast"]["simpleforecast"]["forecastday"][1]["icon"]]
		weatherInfo['tomorrow_precip'] =  self.weather["forecast"]["simpleforecast"]["forecastday"][1]["pop"]

		return weatherInfo

	def getAllDevices(self):
		allDevices = {}
		allDevices["switch"] = self.request_devices("switch")
		allDevices["contact"] = self.request_devices("contact")
		allDevices["lock"] = self.request_devices("lock")
		allDevices["mode"] = self.request_devices("mode")
		allDevices["power"] = self.request_devices("power")
		allDevices["presence"] = self.request_devices("presence")
		allDevices["dimmer"] = self.request_devices("dimmer")
		allDevices["temperature"] = self.request_devices("temperature")
		allDevices["humidity"] = self.request_devices("humidity")
		allDevices["weather"] = self.request_devices("weather")
		allDevices["motion"] = self.request_devices("motion")
		allDevices["color"] = self.request_devices("color")

		return allDevices

	def updateSwitch(self):
		switches = {}
		switches = self.request_devices("switch")

		return switches

	def updateColor(self):
		colors = {}
		colors = self.request_devices("color")
		#print colors

		return colors

	def updatePower(self):
		power = {}
		power = self.request_devices("power")

		return power

	def updateHumidity(self):
		humidity = {}
		humidity = self.request_devices("humidity")

		return humidity

	def updateContact(self):
		contacts = {}
		contacts = self.request_devices("contact")

		return contacts

	def updatePresence(self):
		presence = {}
		presence = self.request_devices("presence")

		return presence

	def updateMotion(self):
		motion = {}
		motion = self.request_devices("motion")

		return motion


	def updateMode(self):
		mode = {}
		mode = self.request_devices("mode")

		return mode

	def updateDimmer(self):
		dimmer = {}
		dimmer = self.request_devices("dimmer")

		return dimmer

	def updateWeather(self):
		weather = {}
		weather = self.request_devices("weather")

		return weather

	def updateTemp(self):
		temperature = {}
		temperature = self.request_devices("temperature")

		return temperature



def printAllDevices(allDevices):
	devicesWithState=['switch','contact','presence','dimmer','motion']
	devicesWithValue=['temperature','humidity','power']
	devicesWithEnergy=['power']
	devicesWithLevel=['dimmer']

	for device in allDevices:
		deviceKeys = allDevices[device].keys()
		print "Device Type: ", device
		for k in deviceKeys:
			if (device != "deviceType" and device != "weather" ):
				print "\t", k, 
				if device in devicesWithState:
					print " - ", allDevices[device][k]['state'],
				if device in devicesWithValue:
					print " - ", allDevices[device][k]['value'],
				if device in devicesWithEnergy:
					print " - ", allDevices[device][k]['energy'],
				if device in devicesWithLevel:
					print " - ", allDevices[device][k]['level'], 
				if device == "mode":
					print  " - ", allDevices[device][k]['mode'],
				print " - ", allDevices[device][k]['deviceType'],
			print ""

def rgbToHsl(hex_value):
	r = int(hex_value[1:3],16)
	g = int(hex_value[3:5],16)
	b = int(hex_value[5:7],16)
	r = float(r) / 255.0
	g = float(g) / 255.0
	b = float(b) / 255.0
	# Calculate the hsl values.
	cmax = max(r, g, b)
	cmin = min(r, g, b)
	delta = cmax - cmin
	# Hue
	if (cmax == r) and (delta > 0):
		h = 60 * (((g - b) / delta) % 6.0)
	elif (cmax == g) and (delta > 0):
		h = 60 * (((b - r) / delta) + 2.0)
	elif (cmax == b) and (delta > 0):
		h = 60 * (((r - g) / delta) + 4.0)
	elif (delta == 0):
		h = 0
	# Lightness
	l = (cmax + cmin) / 2.0
	# Saturation
	if (delta == 0):
		s = 0
	else:
		s = (delta / (1 - abs((2 * l) - 1)))
	s = s * 100.0
	l = l * 100.0
	return {"hue":h, "sat":s, "level":l, "hex":hex_value}

