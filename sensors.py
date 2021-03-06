#Author: Jacob Gasser
#Date: 12/1/20
#Purpose:
# This file is the executing code for the multimodal landslide system. This file handles
# sensor instances, and uses higher level functions and classes that can be found in both 
# hx711.py and PySense.py modules.
import time
import sys
import PySense
import asyncio
import json
#Set up HX711 Driver
EMULATE_HX711=False
if not EMULATE_HX711:
    import RPi.GPIO as GPIO
    from hx711 import HX711
else:
    from emulated_hx711 import HX711

hx1 = PySense.CreateLoadSensor(5,6,1) #Create a Load Sensor
hx2 = PySense.CreateLoadSensor(20,21,1) #Create a Load Sensor
hx3 = PySense.CreateLoadSensor(22,23,1) #Create a Load Sensor
WeightSensor1 = PySense.LoadSensor(hx1) #Place the Load Sensor into a new class that has more functions
WeightSensor2 = PySense.LoadSensor(hx2)
WeightSensor3 = PySense.LoadSensor(hx3)

WEIGHT_SENSORS = [WeightSensor1, WeightSensor2, WeightSensor3]
while True:
    try:
        WeightSensor1.SetWeight(WeightSensor1.CurrWeight) #Read Data from weight sensor 1
        WeightSensor2.SetWeight(WeightSensor2.CurrWeight) 
        WeightSensor3.SetWeight(WeightSensor3.CurrWeight) 
        print("\nCurrent Weight1: " + str(WeightSensor1.GetValue())) #Get Weight From Sensor
        print("\nCurrent Weight2: " + str(WeightSensor2.GetValue())) #Get Weight From Sensor
        print("\nCurrent Weight3: " + str(WeightSensor3.GetValue())) #Get Weight From Sensor

        #Create JSON Object with all working sensors, send this to the DB
        data = '{ '
        for sensor in WEIGHT_SENSORS:
            val =sensor.GetValue()
            if(val != 'NA'):
                data += ' "Weight": "' + val + '",' 
        data = data[0:len(data)-1]
        data += ' }'
        asyncio.run(PySense.SendToDB(data))
        time.sleep(1.25)
    except (KeyboardInterrupt, SystemExit):
        PySense.cleanAndExit()

