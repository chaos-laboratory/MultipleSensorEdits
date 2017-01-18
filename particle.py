from urllib2 import urlopen, URLError  # request,
import csv
import json
import datetime as datetime
import time as time
import requests
import sseclient

# this is the only place you need to put your Particle access token
access_token = 'a29cef4e07f57df80ddcc15fb5857e9fc5b98ce0'

# DEVICES API url
deviceAPI_url = 'https://api.particle.io/v1/devices/?access_token=' + access_token

# EVENTS API url
eventsAPI_url = 'https://api.particle.io/v1/devices/events?access_token=' + access_token

# File suffix
file_suffix = "_data_log.csv"

addressbook = {} # will house id name pairs


def deviceAPICall():
    devices_req = requests.get(deviceAPI_url)
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


def get_core_url(coreID):
    URL = "https://api.particle.io/v1/devices/" + coreID + "/?access_token=" + access_token
    return URL

def get_var_url(coreID, var):
    URL = "https://api.particle.io/v1/devices/" + coreID + "/" + var + "/?access_token=" + access_token
    return URL

def url_json(url):
    req = requests.get(url)
    json = req.json()
    return json

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


#   ***
#   SSE client functions begin here!


def get_duration():
    print "How long would you like to record for? (in seconds)"
    duration = raw_input()
    print "\n"
    duration = int(duration)
    return duration

def get_answer(question):
    print question
    answer = raw_input("\n>>>  ")
    return answer

def str_to_int(variable):
    try:
        variable = int(variable)
    except ValueError:
        print "Not valid...\n"
        variable = -1
    return variable


def get_locations():
    numErrors = 0
    for address in addressbook:
        json = url_json(get_core_url(address))
        print json

        try:
            if json["variables"] is not None:
                if json["variables"].has_key("location"):
                    json = url_json(get_var_url(address,"location"))
                    print json["result"]
            #     json = url_json(get_var_url(address,"location"))
            else:
                print "no variables!"
        except AttributeError:
            print "Attribute Error!! Check out: " + str(get_core_url(address))
            numErrors += 1
        except KeyError:
            print "Key Error!! Check out: " + str(get_core_url(address))
            numErrors += 1

def add_locations():
    numErrors = 0
    for address in addressbook:
        json = url_json(get_core_url(address))
        print json
        try:
            if json["variables"] is not None:
                if json["variables"].has_key("location"):
                    json = url_json(get_var_url(address,"location"))
                    addressbook[address]["location"] = json["result"]
                    print json["result"]
            #     json = url_json(get_var_url(address,"location"))
            else:
                print "no variables!"
        except AttributeError:
            print "Attribute Error!! Check out: " + str(get_core_url(address))
            numErrors += 1
            addressbook[address]["location"] = json["ERROR"]
        except KeyError:
            print "Key Error!! Check out: " + str(get_core_url(address))
            numErrors += 1
            addressbook[address]["location"] = json["ERROR"]
    print "\n\nGot " + str(numErrors) +  " errors!"


def _addressbook():
    print "\nGenerating addressbook..."
    devices = getConnectedDevices()
    for device in devices:
        addressbook[device["id"]] = {}
        addressbook[device["id"]]["name"] = device["name"]
        addressbook[device["id"]]["location"] = "none"
    #get_locations()
    print "\nDone!"
    return addressbook

def update_addressbook():
    devices = getConnectedDevices()
    len_at_start = len(addressbook)
    len_at_end = len(addressbook)
    for device in devices:
        if device["id"] not in addressbook:
            addressbook[device["id"]] = device["name"]
    len_at_end = len(addressbook)
    if len_at_end != len_at_start:
        print "\nAdded " + str(len_at_end - len_at_start) + " device(s)!"



#   this method is the model for option 1
def stream_sse():
    # generates file name
    starttime = datetime.datetime.now().strftime('%m_%d_%Y_%H_%M_%S')
    filename = starttime + file_suffix

    # how long we'll be running the collection for
    lengthofreadings = 0  # zero until user input
    frequency = 0 # in seconds

    # CSV Stuff
    row = []
    dataIndex = []
    nameIndex = []
    header = ["Event","Value","ID","Location"]

    stopWrite = False

    # Ask user for length of collection
    lengthofreadings = get_answer("\nHow long would you like to collect data for? (seconds)")
    lengthofreadings = str_to_int(lengthofreadings)
    end = time.time() + lengthofreadings  # in seconds

    # Generate name look up dict
    addressbook = _addressbook()

    messages = sseclient.SSEClient(eventsAPI_url)
    with open(filename, "a") as file:
        writer = csv.writer(file, delimiter=",")

        # Generate name lookup
        addressbook = _addressbook()

        # writes the column headers
        writer.writerow(header)
        for msg in messages:
            event = str(msg.event)

            if event != 'message':
                row.append(event)
                data = msg.data
                if type(unicode):
                    data_json = json.loads(data)
                    event_value = str(data_json['data'])
                    row.append(event_value)
                    row.append(addressbook[data_json['coreid']])
                    print event_value
                else:
                    pass
                print data


            # if nameIndex:
            #     if event == nameIndex[0]:
            #         if stopWrite == False:  # This is so it only prints once
            #             writer.writerow(nameIndex)
            #             stopWrite = True
            #         writer.writerow(dataIndex)
            #         dataIndex = []
            #
            #
            # # prints out the data
            # outputMsg = msg.data
            # if type(outputMsg) is not str:
            #     data_json = json.loads(outputMsg)
            #     parse_data = str(data_json['data'])
            #     dataIndex.append(parse_data)
            #     print parse_data

            # event: humidity
            # data: {"data": "41.099998", "ttl": "60", "published_at": "2017-01-16T20:07:41.122Z",
            #        "coreid": "3c002f001747353236343033"}

            if time.time() > end:
                print "\ncompleted " + str(lengthofreadings) + " seconds of collection."
                break

            writer.writerow(row)
            row = []
            event_value = ""

_addressbook()