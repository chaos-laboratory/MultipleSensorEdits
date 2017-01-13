from urllib2 import urlopen, URLError  # request,
import csv
import json
import datetime as datetime
import time as time
import requests

# this is the only place you need to put your access token
access_token = 'a29cef4e07f57df80ddcc15fb5857e9fc5b98ce0'


def getConnectedDevices():
    claimedDevices = deviceAPICall()

    indices = []  # will contain indices of connected Particles
    connected_devices = []  # will contain connected Particle metadata

    for index, device in enumerate(claimedDevices):
        if device["connected"] == True:
            #  indices.append(index)
            connected_devices.append(device)

    return connected_devices


def deviceAPICall():
    devices_url = 'https://api.particle.io/v1/devices?access_token=' + access_token
    devices_req = requests.get(devices_url)
    devices_req_json = devices_req.json()
    return devices_req_json


def howManyClaimedDevices():
    claimedDevices = deviceAPICall()
    return len(claimedDevices)


def getConnectedDevices():
    claimedDevices = deviceAPICall()

    indices = []  # will contain indices of connected Particles
    connected_devices = []  # will contain connected Particle metadata

    for index, device in enumerate(claimedDevices):
        if device["connected"] == True:
            #  indices.append(index)
            connected_devices.append(device)

    return connected_devices


def howManyConnectedDevices():
    connected_devices = getConnectedDevices()

    return len(connected_devices)


def listConnectedDevices():
    devices_url = 'https://api.particle.io/v1/devices?access_token=' + access_token
    devices_req = requests.get(devices_url)
    devices_req_json = devices_req.json()

    indices = []
    for index, devices_req_json in enumerate(devices_req_json):
        if devices_req_json["connected"] == True:
            indices.append(index)

    return len(indices)


