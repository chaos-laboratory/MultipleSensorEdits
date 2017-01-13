from urllib2 import urlopen, URLError  # request,
import csv
import json
import datetime as datetime
import time as time
import requests

access_token = 'a29cef4e07f57df80ddcc15fb5857e9fc5b98ce0'


def deviceAPICall():
    devices_url = 'https://api.particle.io/v1/devices?access_token=' + access_token
    devices_req = requests.get(devices_url)
    devices_req_json = devices_req.json()
    return devices_req_json


def howManyClaimedDevices():
    claimedDevices = deviceAPICall()
    return len(claimedDevices)


def connectedDevices():
    pass

def howManyConnectedDevices():
    claimedDevices = deviceAPICall()

    indices = []
    for index, device in enumerate(claimedDevices):
        if device["connected"] == True:
            indices.append(index)

    return len(indices)


def listConnectedDevices():
    devices_url = 'https://api.particle.io/v1/devices?access_token=' + access_token
    devices_req = requests.get(devices_url)
    devices_req_json = devices_req.json()

    indices = []
    for index, devices_req_json in enumerate(devices_req_json):
        if devices_req_json["connected"] == True:
            indices.append(index)

    return len(indices)


