# coding=utf-8
'''
Created on 04.12.2018

@author: bert
'''




import ict3q8 as ict
    

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

res = ict.reqcard(sPort, 2)
if res == 0: # Karte eingesteckt    
    tracklist = ict.check_magstripe(sPort) # Erstmal prüfen, welche Spuren Daten enthalten
    trackset = ict.getalltracks (sPort, tracklist)
    
    for track in [1, 2, 3]:
        if trackset[track-1]:
            print ("Spur {}: {}".format(track, trackset[track-1]))
        else:
            print ("Spur {}: keine Daten".format(track))
else:
    print ("Fehler oder Timeout beim Karte einstecken: {}".format (res))        

ict.ejectcard(sPort)

ict.closeCOM(sPort)
