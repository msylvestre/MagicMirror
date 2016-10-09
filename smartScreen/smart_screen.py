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

# GPIO Config
GPIO.setmode(GPIO.BOARD)

# Pin Initialization
GPIO.setup(config.ECHO_PIN,    GPIO.IN)
GPIO.setup(config.TRIGGER_PIN, GPIO.OUT)
GPIO.setup(config.LED_PIN,     GPIO.OUT)    # Optional


# ---------------------------------------------------------
def measureDistance():
    
    # Initialize the proximity sensor
    GPIO.output(config.TRIGGER_PIN, True)
    time.sleep(0.00001)
    GPIO.output(config.TRIGGER_PIN, False)

    # Loop until ECHO_PIN is 0v 
    while GPIO.input(config.ECHO_PIN) == 0:        
        pass   

    start = time.time()                   

    # Loop until ECHO_PIN is 5v, mean the signal came back
    while GPIO.input(config.ECHO_PIN) == 1:        
        pass

    end = time.time()

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





# =============================================================================
#  MAIN
# =============================================================================

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

            print "Mesured Distance : %.2f cm" % distance
            print "Clean Distance  : %.2f cm" % cleanDistance
            print "---------------------------------------------"
            
            if cleanDistance != -1:    # Check the smoothing is initialized (need 3 value minimum)
               
                if cleanDistance < config.USER_DISTANCE:
                    if currentHdmiState == 'OFF':
                        setDisplay('ON')
                        setLed('ON')
                        currentHdmiState = 'ON'
                    
                    print "LED: ON  Waiting %s second of delay" % config.ENABLE_DELAY
                    time.sleep(config.ENABLE_DELAY)
                    
                elif cleanDistance > 30 and currentHdmiState == 'ON':
                    setDisplay('OFF')
                    setLed('OFF')
                    currentHdmiState = 'OFF'

            time.sleep(config.READ_DELAY)            
            
    finally:
        GPIO.cleanup()
        print "time to quit"    