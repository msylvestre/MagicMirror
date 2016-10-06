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

GPIO.setmode(GPIO.BOARD)

# GPIO Pin 
trig = 38  # sends the signal
echo = 40  # listens for the signal
led  = 11  # Light ON when screen ON.

# Pin Init
GPIO.setup(echo, GPIO.IN)
GPIO.setup(trig, GPIO.OUT)
GPIO.setup(led,  GPIO.OUT)

# Global Variable
DELAY = 5                   # Time to wait before re-reading distance, when the screen switch ON


class SignalNoiseCleaner():

    lastDistance == 0

    def avgArray(arr):

        '''
        totalArr = 0
        avgArr = 0
        
        for i = 0..arr.len:
            totalArr += arr[0]

        avgArr = totalArr / arr.len

        return avgArr

        '''        

    def shiftArray(arr):

        '''


        '''


    def cleanNoise(newDistance):

        '''
        if newDistance > 10% of oldDistance more less than 3 time:
            retrun oldDistance
        '''

    def smoothNoise(newDistance):

        '''
        init array[]

        if array.len <= 2:
            array[array.len] = newDistance
            
            if array.len = 2:
                distance = avgArray(array) / 3
            else:
                distance = -1
        else:
            shift(array)
            array[2] = valueX
            distance = avgArray(array) / 3

        return distance

        '''

        if lastDistance == 0:
            lastDistance = distance
            return distance

        elif distance > 100:
            return lastDistance

        else:
            lastDistance = distance
            return distance


# ---------------------------------------------------------
def measureDistance():
    
    # Initialize the trigger
    GPIO.output(trig, True)
    time.sleep(0.00001)
    GPIO.output(trig, False)

    
    while GPIO.input(echo) == 0:        # Loop until echo is 0v 
        pass   

    start = time.time()                 # reached when echo starts listening  

    while GPIO.input(echo) == 1:        # Loop until echo is 5v, mean the signal came back
        pass

    end = time.time()                   # reached when the signal arrived

    # Calculate the distance and make sure the reading is valid
    distance = ((end - start) * 34300) / 2  # 343m/s is the speed of sound
    
    # snc = SignalNoiseCleaner() 
    # distance = snc.cleanupNoise(distance)
    # distance = snc.smoothSignal(distance)
 
    return distance




# ---------------------------------------------------------
def setLed(state):

    if state == 'ON':
        GPIO.output(led, True)

    elif state == 'OFF':
        GPIO.output(led, False)


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
 
        lastDistance = 0            # Keep the last distance read by the sonar
        currentHdmiState = 'OFF'

        print "Init display to OFF"
        setDisplay('OFF')
        setLed('OFF')


        while True:

            distance = measureDistance() 
            print "distance: %.2f cm" % distance
            
            if distance < 30:
                if currentHdmiState == 'OFF':
                    setDisplay('ON')
                    setLed('ON')
                    currentHdmiState = 'ON'
                
                print "LED: ON  Waiting %s second of delay" % DELAY
                time.sleep(DELAY)
                
            elif distance > 30 and currentHdmiState == 'ON':
                setDisplay('OFF')
                setLed('OFF')
                currentHdmiState = 'OFF'

            time.sleep(1)            

    finally:
        GPIO.cleanup()
    