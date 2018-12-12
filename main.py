# coding=utf-8
'''
Created on 04.12.2018

@author: bert
'''




import ict3q8 as ict
#from time import sleep


    

sPort = ict.openCOM ()
print ("Port {} mit {} bps geöffnet.\nCTS={}, DSR={}\n".format (sPort.name, sPort.baudrate, sPort.cts, sPort.dsr))

res = ict.ict_reset(sPort)
try:
    if res[0]==0:
        print ("Reset: {}".format(res[1]))
    else:
        print ("RESET: Fehler {}".format(res))
        ict.closeCOM(sPort)
        exit (1)

except:
    print ("RESET: Fehler {}".format(res))
    ict.closeCOM(sPort)
    exit (1)

txdata = b"C10"
res = ict.sendICT (sPort, txdata)
if res == ict.ACK:
    rxdata = ict.recvICT(sPort)

txdata = b"C21"
res = ict.sendICT (sPort, txdata)
if res == ict.ACK:
    rxdata = ict.recvICT(sPort)
        
trackset = []
for track in [1, 2, 3]:
    trackdata = ict.read_magstripe(sPort, track)
    if isinstance(trackdata, tuple):
        trackset.append(trackdata[1])
        print ("Daten Spur {}: {}".format(track, trackdata[1].decode()))
         

txdata = b"C@0"
res = ict.sendICT (sPort, txdata)
if res == ict.ACK:
    rxdata = ict.recvICT(sPort)
        
txdata = b"C11"
res = ict.sendICT (sPort, txdata)
if res == ict.ACK:
    rxdata = ict.recvICT(sPort)

txdata = b"CI0"
res = ict.sendICT (sPort, txdata)
if res == ict.ACK:
    rxdata = ict.recvICT(sPort)
    if rxdata[0]==0x50:
        print("ATR: " + "".join(["%02X " % x for x in rxdata[5:]]) + "\n")

txdata = b"CI2"
res = ict.sendICT (sPort, txdata)
if res == ict.ACK:
    rxdata = ict.recvICT(sPort)
    print ("Status: {:2X}\n".format(rxdata[5]))

txdata = b"CI1"
res = ict.sendICT (sPort, txdata)
if res == ict.ACK:
    rxdata = ict.recvICT(sPort)

txdata = b"C@2"
res = ict.sendICT (sPort, txdata)
if res == ict.ACK:
    rxdata = ict.recvICT(sPort)
        
txdata = b"C30"
res = ict.sendICT (sPort, txdata)
if res == ict.ACK:
    rxdata = ict.recvICT(sPort)


ict.closeCOM(sPort)


    
                
    