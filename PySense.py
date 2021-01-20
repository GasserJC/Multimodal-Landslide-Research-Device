#Author: Jacob Gasser
#Date: 12/1/20
#Purpose:
#This File contains all the classes and functions for the sensors.py File:
import time
import sys
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import datetime
import asyncio
import PySense

#This was a test

cred = credentials.Certificate('creds.json') #need IAM credentials file.
firebase_admin.initialize_app(cred)
db = firestore.client()

#
# Classes Section
#

#Load Sensor Class - this will increase readbility, and ease of error handling. 
class LoadSensor:
    def __init__(self, s):
        self.sensor = s
        self.a = 0
        self.b = 0
        self.c = 0
    # If you want to get the current weight
    def GetValue(self):
        if(self.a*self.b*self.c == 0):
            return 'NA'
        else:
            return (self.a+self.b+self.c)/3
    #If you want to set the current weight & Write to DB
    def SetWeight( self, w ):
        if(w != -1):
            self.a = self.b
            self.b = self.c
            self.c = w
        else:
            self.a = 0
            self.b = 0
            self.c = 0
    # Sensor's current reading
    def CurrWeight(self):
        try:
            val = self.sensor.get_weight(5)
            self.sensor.power_down()
            self.sensor.power_up()
            return val
        except:
            return -1

#
# Functions Section
#

#Set up HX711 Driver
EMULATE_HX711=False
if not EMULATE_HX711:
    import RPi.GPIO as GPIO
    from hx711 import HX711
else:
    from emulated_hx711 import HX711

#Exit Function
def cleanAndExit():
    print("Cleaning.")
    if not EMULATE_HX711:
        GPIO.cleanup()
    print("Bye.")
    sys.exit()

#Asynchronous function to write to the cloud database
async def SendToDB(data):
    #JSON object with one key value pair, Grams => (sensor weight)
    db.collection(u'SensorData').document(str(datetime.now())).set(data) #Write into the database

#Creates a Load Sensor Class
def CreateLoadSensor( pin1, pin2, refunit):
    hx = HX711(pin1, pin2)
    hx.set_reading_format("MSB", "MSB")
    hx.set_reference_unit(refunit)
    hx.reset()
    hx.tare()
    return hx