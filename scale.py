import time
import sys
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import datetime
import asyncio

#Log into Cloud Database
cred = credentials.Certificate('creds.json') #need IAM credentials file.
firebase_admin.initialize_app(cred)
db = firestore.client()

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
async def SendToDB( WeightValue ):
    #JSON object with one key value pair, Grams => (sensor weight)
    data = { 
        u'Grams': WeightValue
    }
    db.collection(u'SensorData').document(str(datetime.now())).set(data) #Write into the database

#This sets up the scale, uses pins 5 and 6
hx = HX711(6, 5)

#More set up - this is simply things the driver asks us to set up but does not need to be understood
hx.set_reading_format("MSB", "MSB")

#Load cells return a value based on variation within voltage, the reference unit is a coefficient of that reading.
#Therefore, the reference unit must be emperically found and set to the desired value for your desired unit.
referenceUnit = 1
hx.set_reference_unit(referenceUnit)
hx.reset()
hx.tare()

#Variables for a running avg
a = 0
b = 0
c = 0

while True:
    try:
        #Read Value from sensor
        val = hx.get_weight(5)
        print("\nCurrent Weight: " + str(val))

        #Running Avg
        a = b
        b = c
        c = val
        if( a*b*c != 0):
            print("Avg of 3:       " + str((a+b+c)/3))
        
        #Reset Cell Reading
        hx.power_down()
        hx.power_up()

        #Asynchronously write to the data base with the newest scale value.
        asyncio.run(SendToDB(str((a+b+c)/3)))
        time.sleep(1.25)
        
    except (KeyboardInterrupt, SystemExit):
        cleanAndExit()

