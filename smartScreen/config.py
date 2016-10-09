#!/usr/bin/python

# Pi Config - GPIO Pin 
TRIGGER_PIN = 38            # sends the signal
ECHO_PIN    = 40            # listens for the signal
LED_PIN     = 11            # Light ON when screen ON.


# Smart Screen Config
READ_DELAY    = 0.2         # Delay between each reading of the sensor, when screen is OFF
ENABLE_DELAY  = 3           # Time to wait before re-reading distance, when the screen switch ON
USER_DISTANCE = 45          # Distance in cm where the user should be, at the minimum, to enable the display
