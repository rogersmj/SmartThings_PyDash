#! /usr/bin/python
#################################################
#        SmartThings Dashboard interface		#
#################################################
# Matt Rogers - 2015	 						#
# matt@rogersmj.com								#
#												#
# Features: 									#
#	- UI interface methods for the Dashboard	#
#	- Connects Dashboard widgets to SmartThings #
#		API. 									#
#################################################
#################################################

import sys
import requests
import pprint
import json
import os

from urllib import quote

import smartthings_api

stInitd = False
selectedHue = None
selectedDimmer = None
hostURL = None

class Dashboard(object):
	def __init__(self, authfile):
		self.Initd = False
		self.api = smartthings_api.SmartThings()

		oauthIn = {}
		with open(authfile) as oauthfile:
			oauthIn = json.load(oauthfile)
		self.hostURL = oauthIn['host_url']

	def apiAuthorized():
		return api.isAuthorized()

	def initAuthorization(url):
		return api.authURL(url)

	def hostURL():
		return self.hostURL



def initST():
	global stInitd
	global smartThings
	global allDevices
	stInitd = False
	smartThings = smartthings_api.SmartThings()

def setHostUrl(filename="oauthin.json"):
	global hostURL
	oauthIn = {}
	with open(filename) as oauthfile:
		oauthIn = json.load(oauthfile)
	hostURL = oauthIn['host_url']

def getHostUrl():
	global hostURL
	return hostURL



def initd():
	global stInitd
	return stInitd




def init():
	global stInitd
	global smartThings
	global allDevices
	stInitd = True

	#smartThings = smartthings_api.SmartThings()
	smartThings.load_settings()
	smartThings.request_endpoints()

	allDevices = smartThings.getAllDevices()



def getAllDeviceType(deviceType):
	global allDevices
	return allDevices[deviceType]

def getDevice(deviceType, deviceId):
	global allDevices
	return allDevices[deviceType][deviceId]

def getDeviceStatus(deviceType, deviceId, deviceStatus):
	global allDevices
	device = getDevice(deviceType,deviceId)
	return device[deviceStatus]

def setSelectedHue(deviceId):
	global selectedHue
	selectedHue = deviceId

def getSelectedHue():
	global selectedHue
	return selectedHue

def setSelectedDimmer(deviceId):
	global selectedDimmer
	selectedDimmer = deviceId

def getSelectedDimmer():
	global selectedDimmer
	return selectedDimmer

def setColor(deviceId,color):
	global smartThings

	results = smartThings.set_color(deviceId,color)
	return results

def setColorHSLA(deviceId,hue,sat,color):
	global smartThings

	results = smartThings.set_color_hsla(deviceId,hue,sat,color)
	return results

def updateAll():
	global allDevices
	global smartThings

	allDevices = smartThings.getAllDevices()

def updateSwitch():
	global allDevices
	global smartThings

	allDevices['switch'] = smartThings.updateSwitch()

def updateColor():
	global allDevices
	global smartThings

	allDevices['color'] = smartThings.updateColor()

def updateContact():
	global allDevices
	global smartThings

	allDevices['contact'] = smartThings.updateContact()

def updatePresence():
	global allDevices
	global smartThings

	allDevices['presence'] = smartThings.updatePresence()

def updateHumidity():
	global allDevices
	global smartThings

	allDevices['humidity'] = smartThings.updateHumidity()

def updatePower():
	global allDevices
	global smartThings

	allDevices['power'] = smartThings.updatePower()

def updateMotion():
	global allDevices
	global smartThings

	allDevices['motion'] = smartThings.updateMotion()

def toggleSwitch(deviceId):
	global smartThings
	global allDevices

	newState = smartThings.command_switch(deviceId, 't')
	allDevices['switch'][deviceId]['state'] = newState
	allDevices['switch'] = smartThings.updateSwitch()

def setSwitch(deviceId,state):
	global smartThings
	global allDevices

	newState = smartThings.command_switch(deviceId, state)
	allDevices['switch'][deviceId]['state'] = state
	allDevices['switch'] = smartThings.updateSwitch()


def getMode():
	global allDevices
	return allDevices['mode']['Mode']['mode']

def updateMode():
	global allDevices
	global smartThings

	allDevices['mode'] = smartThings.updateMode()

def setMode(mode):
	global allDevices
	global smartThings

	smartThings.command_mode(mode)


def updateDimmer():
	global allDevices
	global smartThings

	allDevices['dimmer'] = smartThings.updateDimmer()

def setDimmer(deviceId,level):
	global allDevices
	global smartThings

	smartThings.command_dimmer(deviceId,level)
	allDevices['dimmer'][deviceId]['level'] = level
	allDevices['dimmer'] = smartThings.updateDimmer()

def getWeather():
	global smartThings

	return smartThings.get_weather()

def updateWeather():
	global allDevices
	global smartThings

	allDevices['weather'] = smartThings.updateWeather()

def updateTemp():
	global allDevices
	global smartThings

	allDevices['temperature'] = smartThings.updateTemp()

