#!/usr/bin/python3
# coding=utf-8
'''
Created on 04.12.2018

@author: bert
'''


import ict3q8 as ict

amex_tr1 = b'2B3739 531923 51004^AMEX TEST CARD ANSI       ^2103150412345'
amex_tr2 = b'2373953192351004=2103150412345'

sPort = ict.openCOM ()
print ("Port {} mit {} bps geöffnet.\nCTS={}, DSR={}\n".format (sPort.name, sPort.baudrate, sPort.cts, sPort.dsr))

res = ict.ict_reset(sPort)
try:
    if res[0]==0:
        print ("Reset: {}{}".format(res[1], res[2]))
    else:
        print ("RESET: Fehler {}{}".format(res[1], res[2]))
        ict.closeCOM(sPort)
        exit (1)

except:
    print ("RESET: Fehler {}".format(res))
    ict.closeCOM(sPort)
    exit (1)



res = ict.reqcard(sPort, 0)
if res == 0: # Karte eingesteckt und in Position?    
    tracklist = ict.check_magstripe(sPort) # Erstmal prüfen, welche Spuren Daten enthalten
    trackset = ict.gettracks (sPort, tracklist)
    
    for track in [1, 2, 3]:
        if trackset[track-1]:
            print ("Spur {}: {}".format(track, trackset[track-1]))
        else:
            print ("Spur {}: keine Daten".format(track))
else:
    print ("Fehler oder Timeout beim Karte einstecken: {}".format (res))        

'''
ict.ejectcard(sPort)

print ("Leere Karte einschieben!")

res = ict.reqcard(sPort, 0)
if res == 0:
    ict.cleartrackbuf(sPort)

    res = ict.writetrackbuf(sPort, 1, amex_tr1)
    print (res)
    res = ict.writetrackbuf(sPort, 2, amex_tr2)
    print (res)
    re = ict.writealltracks(sPort)
    print (res)
else:
    print ("Fehler oder Timeout beim Karte einstecken: {}".format (res))        


for track in [1, 2, 3]:
    if trackset[track-1]:
        print ("Schreibe Puffer Spur {}: ".format (track), end="")
        res = ict.writetrackbuf(sPort, track, trackset[track-1])
        print (res)
'''
    
ict.ejectcard(sPort)
ict.closeCOM(sPort)
