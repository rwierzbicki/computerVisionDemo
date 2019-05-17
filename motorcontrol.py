import RPi.GPIO as GPIO
import time


FWD = 17
PWM = 27
BACK = 22

RIGHT = 5
LEFT = 12
lastTurn = 0

GPIO.setmode(GPIO.BCM)
GPIO.setup(PWM, GPIO.OUT)
GPIO.setup(LEFT, GPIO.OUT)
GPIO.setup(RIGHT, GPIO.OUT)
speed = GPIO.PWM(PWM, 100)
Lturn = GPIO.PWM(PWM, 100)
Rturn = GPIO.PWM(PWM, 100)

def motorSetup():
    GPIO.setwarnings(False)

    GPIO.setup(FWD, GPIO.OUT)
    GPIO.setup(BACK, GPIO.OUT)
    GPIO.setup(RIGHT, GPIO.OUT)
    GPIO.setup(LEFT, GPIO.OUT)
    speed.start(0)
    speed.ChangeFrequency(10000)
    Lturn.ChangeFrequency(10000)
    Rturn.ChangeFrequency(10000)

def setSpeed(velocity):
    GPIO.output(FWD, GPIO.LOW)
    GPIO.output(BACK, GPIO.LOW)

    speed.ChangeDutyCycle(abs(velocity))
    GPIO.output(FWD, GPIO.HIGH) if velocity >= 0 else GPIO.output(BACK, GPIO.HIGH)

def setTurn(turn):

    if(turn  <9 and turn>-9):
        GPIO.output(RIGHT, GPIO.LOW)
        GPIO.output(LEFT, GPIO.LOW)
    if turn > 10:
        GPIO.output(LEFT, GPIO.LOW)
        GPIO.output(RIGHT, GPIO.HIGH)

    if turn < -10: 
        GPIO.output(RIGHT, GPIO.LOW)
	GPIO.output(LEFT, GPIO.HIGH)
    lastTurn = turn
