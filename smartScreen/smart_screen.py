#!/usr/bin/python

# =========================================================
# Smart Screen
#
# - Manage the screen ON/OFF when a person approach closer
#   than 30 cm of the mirror
#
# =========================================================

import RPi.GPIO as GPIO
import time
import subprocess
import signalNoiseCleaner as sncModule
import config

GPIO.setmode(GPIO.BOARD)

# Pin Init
GPIO.setup(config.ECHO_PIN, GPIO.IN)
GPIO.setup(config.TRIGGER_PIN, GPIO.OUT)
GPIO.setup(config.LED_PIN,  GPIO.OUT)





# ---------------------------------------------------------
def measureDistance():
    
    # Initialize the TRIGGER_PINger
    GPIO.output(config.TRIGGER_PIN, True)
    time.sleep(0.00001)
    GPIO.output(config.TRIGGER_PIN, False)

    
    while GPIO.input(config.ECHO_PIN) == 0:        # Loop until ECHO_PIN is 0v 
        pass   

    start = time.time()                 # reached when ECHO_PIN starts listening  

    while GPIO.input(config.ECHO_PIN) == 1:        # Loop until ECHO_PIN is 5v, mean the signal came back
        pass

    end = time.time()                   # reached when the signal arrived

    # Calculate the distance and make sure the reading is valid
    distance = ((end - start) * 34300) / 2  # 343m/s is the speed of sound
    
    return distance



# ---------------------------------------------------------
def setLed(state):

    if state == 'ON':
        GPIO.output(config.LED_PIN, True)

    elif state == 'OFF':
        GPIO.output(config.LED_PIN, False)


# ---------------------------------------------------------
def setDisplay(hdmiState):

    if hdmiState == 'ON':
        subprocess.call('sh hdmi_on.sh', shell=True)
        print "Change HDMI State to ON"

    elif hdmiState == 'OFF':
        subprocess.call('sh hdmi_off.sh', shell=True)
        print "Change HDMI State to OFF"

    return hdmiState





# =========================================================
#  MAIN
# =========================================================

if __name__ == '__main__':  

    try:

        snc = sncModule.SignalNoiseCleaner() 
        
        currentHdmiState = 'OFF'

        print "Init display to OFF"
        setDisplay('OFF')
        setLed('OFF')


        while True:

            
            distance = measureDistance() 
            cleanDistance = snc.cleanNoise(distance)
            
            #smoothDistance = snc.smoothNoise(distance)
            smoothDistance = cleanDistance

            print "Mesured Distance : %.2f cm" % distance
            print "Clean Distance  : %.2f cm" % cleanDistance
            print "Smooth Distance  : %.2f cm" % smoothDistance
            print "---------------------------------------------"
            
            if smoothDistance != -1:    # Check the smoothing is initialized (need 3 value minimum)
               
                if smoothDistance < config.USER_DISTANCE:
                    if currentHdmiState == 'OFF':
                        setDisplay('ON')
                        setLed('ON')
                        currentHdmiState = 'ON'
                    
                    print "LED: ON  Waiting %s second of delay" % config.ENABLE_DELAY
                    time.sleep(config.ENABLE_DELAY)
                    
                elif smoothDistance > 30 and currentHdmiState == 'ON':
                    setDisplay('OFF')
                    setLed('OFF')
                    currentHdmiState = 'OFF'

            time.sleep(config.READ_DELAY)            
            
    finally:
        GPIO.cleanup()
        print "time to quit"    