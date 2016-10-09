#!/usr/bin/python

# =========================================================
# Smart Screen
#
# - Manage the screen ON/OFF when a person approach closer
#   than 30 cm of the mirror
#
# =========================================================

#import RPi.GPIO as GPIO
import time
import subprocess

#GPIO.setmode(GPIO.BOARD)

# GPIO Pin 
trig = 38  # sends the signal
echo = 40  # listens for the signal
led  = 11  # Light ON when screen ON.

# Pin Init
#GPIO.setup(echo, GPIO.IN)
#GPIO.setup(trig, GPIO.OUT)
#GPIO.setup(led,  GPIO.OUT)

# Global Variable
DELAY = 5                   # Time to wait before re-reading distance, when the screen switch ON


class SignalNoiseCleaner():

    smoothDistance = 0
    smoothingBuffer = 3
    arr = []


    def avgArray(self, arr):
        
        totalArr = 0
        avgArr   = 0
        
        for i in range(len(arr)):
            totalArr += arr[i]

        avgArr = totalArr / len(arr)

        return avgArr

                

    def shiftArray(self, arr):

        shiftedArr = []

        # Pop out the first value, move the other to the beginning of the array
        # to make space for a new value
        for i in range(len(arr) - 1):
            shiftedArr.append(arr[i + 1])

        return shiftedArr


    def cleanNoise(self, newDistance):

        '''
        if newDistance > 10% of oldDistance more less than 3 time:
            retrun oldDistance
        '''

    def smoothNoise(self, newDistance):

        if len(SignalNoiseCleaner.arr) < SignalNoiseCleaner.smoothingBuffer - 1:
            SignalNoiseCleaner.arr.append(newDistance)
            SignalNoiseCleaner.smoothDistance = -1
            
        else:

            if SignalNoiseCleaner.smoothDistance == -1:
                SignalNoiseCleaner.arr.append(newDistance)
                SignalNoiseCleaner.smoothDistance = self.avgArray(SignalNoiseCleaner.arr)

            else:
                SignalNoiseCleaner.arr = self.shiftArray(SignalNoiseCleaner.arr)
                SignalNoiseCleaner.arr.append(newDistance)
                SignalNoiseCleaner.smoothDistance = self.avgArray(SignalNoiseCleaner.arr)

        return SignalNoiseCleaner.smoothDistance


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

        snc = SignalNoiseCleaner() 
        print "smoothDistance : ", snc.smoothNoise(15)
        print "smoothDistance : ", snc.smoothNoise(25)
        print "smoothDistance : ", snc.smoothNoise(50)
        print "smoothDistance : ", snc.smoothNoise(50)

 
        
        lastDistance = 0            # Keep the last distance read by the sonar
        currentHdmiState = 'OFF'

        print "Init display to OFF"
        setDisplay('ON')
        setLed('ON')


        while True:

            #distance = snc.smoothNoise(measureDistance())
            distance = measureDistance() 
            print "distance: %.2f cm" % distance
            time.sleep(2)
        
            '''    
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
            '''
    finally:
        #GPIO.cleanup()
        print "time to quit"    