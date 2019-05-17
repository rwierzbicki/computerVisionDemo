#!/usr/bin/python
#encoding: utf-8

import RPi.GPIO as GPIO

#LED Pins
LEDs = [6, 5, 22, 27, 17]

pwmLED = []

# Setup for all LED GPIO Pins.
def LEDSetup():
    pos = 0
    for pin in LEDs:

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.OUT)
	pwmLED.append(GPIO.PWM(pin,100))
	pwmLED[pos].start(0)
	pos += 1

# States:
# 0 = Green
# 1 = Yellow
# 2 = Red
def setLEDState(val):
    
    for pin in pwmLED:
	pin.ChangeDutyCycle(0)

    c = val // 25
    pwmLED[c].ChangeDutyCycle(100-4*(val%25))
    if(c!=4):
        pwmLED[c+1].ChangeDutyCycle(4*(val%25))



if __name__ == "__main__":
    import time
    LEDSetup()
    for i in range(99):
   	 setLEDState(i)
   	 print(i)
    	 time.sleep(0.05)
	
