# Author: Riley Redfern
# Date: 5/4/2021
# Purpose: This file is meant to handle the code that would be used for
# The multiplexer and its interactions with the scales hooked up to its
# The scales need to be calibrated and code needs to be adjusted a lot here

import qwiic as q
import PyNAU7802
import smbus2

multiplex = q.QwiicTCA9548A()
scale = PyNAU7802.NAU7802()
bus = smbus2.SMBus(1)

multiplex.enable_channels(4)

multiplex.list_channels()

#multiplex.disable_channels(4)

if scale.begin(bus):
    print("\nConnected scale successfully\n")
else:
    print("\nCannot connect to scale, exiting\n")
    exit()

currentReading = scale.getReading()
currentWeight = scale.getWeight()

print("Current weight is {0:0.3f}".format(currentWeight))
print("Current reading is {0:0.3f}".format(currentReading))