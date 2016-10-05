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


# ---------------------------------------------------------
def measure_distance():
    
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
    #distance = cleanup_noise(distance)

    return distance


# ---------------------------------------------------------
def cleanup_noise(distance):

    if lastDistance == 0:
        lastDistance = distance
        return distance

    elif distance > 3000:
        return lastDistance

    else:
        lastDistance = distance
        return distance


# ---------------------------------------------------------
def set_led(state):

    if state == 'ON':
        GPIO.output(led, True)

    elif state == 'OFF':
        GPIO.output(led, False)


# ---------------------------------------------------------
def set_display(hdmiState):

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
        set_display('OFF')
        set_led('OFF')


        while True:

            distance = measure_distance() 
            print "distance: %.2f cm" % distance
            
            if distance < 30:
                if currentHdmiState == 'OFF':
                    set_display('ON')
                    set_led('ON')
                    currentHdmiState = 'ON'
                
                print "LED: ON  Waiting %s second of delay" % DELAY
                time.sleep(DELAY)
                
            elif distance > 30 and currentHdmiState == 'ON':
                set_display('OFF')
                set_led('OFF')
                currentHdmiState = 'OFF'

            time.sleep(1)            

    finally:
        GPIO.cleanup()
    