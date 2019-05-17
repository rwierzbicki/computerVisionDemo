#!/usr/bin/python
#encoding: utf-8


import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

#SPI pins
SPICLK = 11
SPIMISO = 9
SPIMOSI = 10
SPICSO = 8

#set up as output
GPIO.setup([SPIMOSI, SPICLK, SPICSO], GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)

#potentiometer connectionto adc intiialized
adc1 = 0
adc2 = 1

#read spi data from mcp3004
def readadc(adcnum, clockpin, mosipin, misopin, cspin):
	if((adcnum>3) or (adcnum<0)):
		return -1
	GPIO.output(cspin, True)
	GPIO.output(clockpin, False)
	GPIO.output(cspin, False)
	commandout = adcnum
	commandout |= 0x18
	commandout <<= 3
	for i in range(5):
		if(commandout & 0x80):
			GPIO.output(mosipin, True)
		else:
			GPIO.output(mosipin, False)
		commandout <<=1
		GPIO.output(clockpin, True)
		GPIO.output(clockpin, False)
	adcout =0

	#read in one empty bit, one null bit, and 10 adc bits
	for i in range(12):
		GPIO.output(clockpin, True)
		GPIO.output(clockpin, False)
		adcout <<=1
		if (GPIO.input(misopin)):
			adcout |=0x1
	GPIO.output(cspin, True)

	adcout >>=1 #first bit is null, shift past it
	return adcout

def read_potentiometer():
	trim_pot = readadc(potentiometer_ad, SPICLK, SPIMOSI, SPIMISO, SPICSO)
	return round(trim_pot/1024.0, 2)
	
if __name__ == "__main__":
	import time
	from led import *
	LEDSetup()
	while True:
		first_pot = readadc(adc1, SPICLK, SPIMOSI, SPIMISO, SPICSO)
		print("first_pot: ", first_pot)
		second_pot = readadc(adc2, SPICLK, SPIMOSI, SPIMISO, SPICSO)
		print("second_pot: ", second_pot)
		val = 100-(((first_pot)-395)/4.20)
		setLEDState( int(val)  )
		time.sleep(0.1)


