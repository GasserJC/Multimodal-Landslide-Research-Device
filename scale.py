import time
import sys

EMULATE_HX711=False

if not EMULATE_HX711:
    import RPi.GPIO as GPIO
    from hx711 import HX711
else:
    from emulated_hx711 import HX711

def cleanAndExit():
    print("Cleaning.")

    if not EMULATE_HX711:
        GPIO.cleanup()
        
    print("Bye.")
    sys.exit()

hx = HX711(6, 5)

hx.set_reading_format("MSB", "MSB")
referenceUnit = 1
hx.set_reference_unit(referenceUnit)
hx.reset()
hx.tare()

a = 0
b = 0
c = 0

while True:
    try:
        val = hx.get_weight(5)
        print("\nCurrent Weight: " + str(val))
        a = b
        b = c
        c = val
        if( a*b*c != 0):
            print("Avg of 3:       " + str((a+b+c)/3))
        
        hx.power_down()
        hx.power_up()
        time.sleep(1.25)
    except (KeyboardInterrupt, SystemExit):
        cleanAndExit()

