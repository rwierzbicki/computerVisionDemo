#!/usr/bin/python
#encoding: utf-8

import btconn
import bluetooth
import time
import motorcontrol as mctl

if __name__ == "__main__":
    serverSock, clientSock = btconn.serverconnect(1, btconn.bdCarAddr, bluetooth.RFCOMM)
    mctl.motorSetup()
    mctl.setSpeed( 20 )
    time.sleep(.1)
    mctl.setSpeed(0)
    while True:
        data = clientSock.recv(32)
        control = data.split(' ')
	if(len(control)>=3):
            mctl.setSpeed( int(control[1]) )
            mctl.setTurn ( int(control[2]) )
	time.sleep(0.05)
