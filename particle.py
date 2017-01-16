from urllib2 import urlopen, URLError  # request,
import csv
import json
import datetime as datetime
import time as time
import requests
import sseclient

# this is the only place you need to put your Particle access token
access_token = 'a29cef4e07f57df80ddcc15fb5857e9fc5b98ce0'

# DEVICE API url
deviceAPI_url = 'https://api.particle.io/v1/devices/?access_token=' + access_token

# EVENTS API url
eventsAPI_url = 'https://api.particle.io/v1/devices/events?access_token=' + access_token

# File suffix
file_suffix = "_data_log.csv"


def deviceAPICall():
    devices_req = requests.get(deviceAPI_url)
    print "did we get this far?"
    devices_req_json = devices_req.json()
    return devices_req_json


def ClaimedDevices():
    claimedDevices = deviceAPICall()
    return claimedDevices


def getConnectedDevices():
    claimedDevices = deviceAPICall()

    connected_devices = []  # will contain connected Particle metadata

    for index, device in enumerate(claimedDevices):
        if device["connected"] == True:
            connected_devices.append(device)

    return connected_devices


def howManyConnectedDevices():
    connected_devices = getConnectedDevices()

    return len(connected_devices)


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


def get_duration():
    print "How long would you like to record for? (in seconds)"
    duration = raw_input()
    print "\n"
    duration = int(duration)
    return duration

def stream_sse():
    starttime = datetime.datetime.now().strftime('%m_%d_%Y_%H_%M_%S')
    filename = starttime + file_suffix

    lengthofreadings = 0  # zero until user input
    end = time.time() + lengthofreadings  # in seconds

    dataIndex = []
    nameIndex = []

    stopWrite = False

    messages = sseclient.SSEClient(deviceAPI_url)
    with open(filename, "a") as file:
        writer = csv.writer(file, delimiter=",")
        for msg in messages:

            # prints out the event
            event = str(msg.event)
            # print event + str(nameIndex[0])
            if nameIndex:
                if event == nameIndex[0]:
                    if stopWrite == False:  # This is so it only prints once
                        writer.writerow(nameIndex)
                        stopWrite = True
                    writer.writerow(dataIndex)
                    dataIndex = []

            if event != 'message':
                print event
                nameIndex.append(event)

            # prints out the data
            outputMsg = msg.data
            if type(outputMsg) is not str:
                data_json = json.loads(outputMsg)
                parse_data = str(data_json['data'])
                dataIndex.append(parse_data)
                print parse_data

            if time.time() > end:
                print "completed " + str(lengthofreadings) + " seconds of collection."
                break

