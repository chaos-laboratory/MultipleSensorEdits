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

    connected_devices = []  # will contain connected Particle metadata

    for index, device in enumerate(claimedDevices):
        if device["connected"] == True:
            connected_devices.append(device)

    return connected_devices


def deviceAPICall():
    devices_url = 'https://api.particle.io/v1/devices?access_token=' + access_token
    devices_req = requests.get(devices_url)
    devices_req_json = devices_req.json()
    return devices_req_json


def ClaimedDevices():
    claimedDevices = deviceAPICall()
    return claimedDevices


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


def print_list(_list):
    for i in _list:
        print i


def truncate_strings(_strings, cut_mark):
    truncated_strings = [string[cut_mark:] for string in _strings]
    return truncated_strings


def strings_to_ints(_list):
    _list = [int(item) for item in _list]
    return _list


def json_sort(_list, _key):
    # this function will sort a list of JSON using values of one key
    keys = [item[_key] for item in _list]
    keys = truncate_strings(keys, 8)
    keys = strings_to_ints(keys)
    keys, _list = (list(t) for t in zip(*sorted(zip(keys, _list))))

    return _list


def list_claimed_devices():
    claimed_devices = ClaimedDevices()
    print "There are " + str(len(claimed_devices)) + " claimed Particles.\n"
    sorted_devices = json_sort(claimed_devices, "name")

    for device in sorted_devices:
        print device["name"] + "   ID: " + device["id"]

def list_connected_devices():
    connected_devices = getConnectedDevices()
    if not connected_devices:
        print "There are NO connected Particles"
    else:
        print "\nThere are " + str(len(connected_devices)) + " connected Particles."
        print "They are:\n"
        #  sort JSON
        sorted_devices = json_sort(connected_devices, "name")
        for device in sorted_devices:
            print device["name"] + "   ID: " + device["id"]