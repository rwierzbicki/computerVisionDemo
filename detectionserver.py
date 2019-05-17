#!/usr/bin/python
#encoding: utf-8

import btconn
import led
import bluetooth
import time

if __name__ == "__main__":

    led.LEDSetup()
    serverSock, clientSock = btconn.serverconnect(0x100F, btconn.bdBaseAddr, bluetooth.L2CAP)

    while True:
	
	state = clientSock.recv(8)
	led.setLEDState(int(state))
	time.sleep(.025)

