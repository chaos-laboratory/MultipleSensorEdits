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

import particle as devices

# Global definitions
access_token = 'a29cef4e07f57df80ddcc15fb5857e9fc5b98ce0'
particle_url = 'https://api.particle.io/v1/devices/events?access_token=' + access_token
starttime = datetime.datetime.now().strftime('%m_%d_%Y_%H_%M_%S')
filename = starttime + "datalogger_test.csv"

lengthofreadings = 0  # seconds
end = time.time() + lengthofreadings  # in seconds

dataIndex = []
nameIndex = []

stopWrite = False


def getDuration():
    print "How long would you like to record for? (in seconds)"
    duration = raw_input()
    print "\n"
    duration = int(duration)
    return duration


print '\nMultiple DHT22 Data Read v2\n\n'

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



