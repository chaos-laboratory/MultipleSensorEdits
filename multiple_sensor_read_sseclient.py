# This version differs in that instead of accessing the API of each photon
# individually, we instead "subscribe" to the data that is being published
# from the dashboard. (https://api.particle.io/v1/devices/events?access_token=a29cef4e07f57df80ddcc15fb5857e9fc5b98ce0)

# Got code to print out data from user Jay L
# (http://stackoverflow.com/questions/29550426/how-to-parse-output-from-sse-client-in-python)

# V1.0 by Jimmy
# V1.5 by James C.

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
    userResponse = raw_input("\n>>>  ")
    try:
        userResponse = int(userResponse)
    except ValueError:
        print "Not valid...\n"
        getTask()

    if userResponse == 1:
        particle.stream_sse()
        getTask()
    elif userResponse == 2:
        particle.list_connected_devices()
        getTask()
    elif userResponse == 4:
        particle.list_claimed_devices()
        getTask()
    else:
        print "Not valid...\n"
        getTask()

getTask()
