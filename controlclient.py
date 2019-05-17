import bluetooth
import btconn
import potentiometer as pt
import time

if __name__ == "__main__":

    socket = btconn.clientconnect(1, btconn.bdCarAddr, bluetooth.RFCOMM)
    recent_speed = 610
    recent_turn = 563
    while True:
	firstPot = pt.readadc(pt.adc1, pt.SPICLK, pt.SPIMOSI, pt.SPIMISO, pt.SPICSO)
        secondPot = pt.readadc(pt.adc2, pt.SPICLK, pt.SPIMOSI, pt.SPIMISO, pt.SPICSO)
	
	
	# Sets the value of the position from -100 to 100
        if( abs(recent_turn - firstPot) > 400): fistPot = recent_turn
	if(abs(recent_speed - secondPot) > 400): secondPot = recent_speed
	pos1 = -2*max(min(100,(firstPot // 8)),0) + 136
	pos2 =  2*max(min(100,(secondPot // 8)),0) - 140 	
	if(pos1>-5 and pos1<5): pos1=0
	if(pos2>-15 and pos2<15): pos2=0
	print("pos1 %d pos2 %d " %( pos1,pos2))

	socket.send(" "+str(pos2)+" "+str(pos1))
	recent_speed = secondPot
	recent_turn = firstPot

	time.sleep(.05)

