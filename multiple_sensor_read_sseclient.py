# This version differs in that instead of accessing the API of each photon
# individually, we instead "subscribe" to the data that is being published
# from the dashboard. (https://api.particle.io/v1/devices/events?access_token=a29cef4e07f57df80ddcc15fb5857e9fc5b98ce0)

# Got code to print out data from user Jay L
# (http://stackoverflow.com/questions/29550426/how-to-parse-output-from-sse-client-in-python)

# V1.0 by Jimmy
# V1.5 by James C.

import sseclient
import pandas as pd
import csv
import requests
import json
import time
import datetime

#  CHAOS developed script
import particle as particle

# Global definitions
access_token = particle.access_token


#  access_token = 'a29cef4e07f57df80ddcc15fb5857e9fc5b98ce0'
particle_url = 'https://api.particle.io/v1/devices/events?access_token=' + access_token
starttime = datetime.datetime.now().strftime('%m_%d_%Y_%H_%M_%S')
filename = starttime + "datalogger_test.csv"

lengthofreadings = 0  # zero until user input
end = time.time() + lengthofreadings  # in seconds

dataIndex = []
nameIndex = []

stopWrite = False

#  These are the users options
functions = ["Log Data", "Check Connected Devices", "Print Outputs", "Check Claimed Devices"]


#  Welcome User
print '\nMultiple DHT22 Data Read v2\n'

#  Get task
def getTask():
    print '\nWhat would you like to do?\n'
    for index, function in enumerate(functions):
        print str(index+1) + ". " + function
    print "\n>>>",
    userResponse = int(raw_input())

    if userResponse == 1:
        pass
    elif userResponse == 2:
        connected_devices = particle.getConnectedDevices()
        print "\nThere are " + str(len(connected_devices)) + " connected Particles."
        print "They are:\n"

        #  sort JSON
        sorted_devices = particle.json_sort(connected_devices, "name")
        for device in sorted_devices:
            print device["name"] + "   ID: " + device["id"]

        getTask()

    elif userResponse == 4:
        claimed_devices = particle.ClaimedDevices()
        print "There are " + str(len(claimed_devices)) + " claimed Particles.\n"
        sorted_devices = particle.json_sort(claimed_devices, "name")

        for device in sorted_devices:
            print device["name"] + "   ID: " + device["id"]

        getTask()

    else:
        print "Not valid...\n"
        getTask()

getTask()



def getDuration():
    print "How long would you like to record for? (in seconds)"
    duration = raw_input()
    print "\n"
    duration = int(duration)
    return duration


lengthofreadings = getDuration()
end = time.time() + lengthofreadings  # in seconds

messages = sseclient.SSEClient(particle_url)
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



