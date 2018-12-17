# coding=utf-8
'''
Created on 07.12.2018

@author: bert
'''

import ict3q8 as ict
from time import sleep


def ict_reset (ser):
    '''
    Sendet RESET zum Leser
    '''    
    txdata = b"C0032400001000"
    res = ict.sendrecvICT (ser, txdata)
    return res


def check_status (ser):
    '''
    Prüft Leserstatus
    Return: ST1, ST0
    '''
    cnt = ict.COMRETRIES
    while cnt:
        txdata = b"C10" # Reader Status?
        res = ict.sendICT (ser, txdata)
        if res == ict.ACK:
            rxdata = ict.recvICT(ser)
            return (rxdata[3] & 0x0F, rxdata[4] & 0x0F)
        else:
            cnt -= 1
            sleep(ict.COMTIMEOUT)
    return -1
        


def check_magstripe (ser):
    '''
    Prüft, welche Magnetspur Daten enthält.
    Return: 3-elementige Liste mit 0x30 = keine Daten, 0x31 = Daten für jede Spur
    '''
    txdata = b"C67"
    if ict.sendICT(ser, txdata) == ict.ACK:
        rxdata = ict.recvICT(ser)
    if rxdata[0]==0x50:
        return rxdata[5:8]
    else:
        return -1
   


def read_magstripe (ser, track):
    '''
    Liest angegebenen Magnetstreifen
    Return: Tuple mit Status und Spurdaten
            1 : Fehler
    '''
    if track in [1, 2, 3]:
        txdata = b"C6" + bytes([track+0x30]) # Lesekommando aufbauen
        if ict.DEBUG:
            print (txdata)
        res = ict.sendICT (ser, txdata)
        if res == ict.ACK:
            rxdata = ict.recvICT(ser)
        if rxdata[0]==0x50: # 'P'
            return (0, rxdata[4:])
        else:
            print ("Fehler: {}\n".format(rxdata.decode()))
            return 1
    else:
        return 1
    
def reqcard (ser, modus, timeout=ict.CARDINTIMER):
    '''
    Setzt ICT-Status ENABLED oder DISABLED
    Modus:   0 = Karte annehmen, auch wenn Magnetstreifen am Prehead ungültig
             1 = Kartenannahme gesperrt
             2 = Karte annehmen, wenn Magnetdaten am Prehead erkannt.
    Return:  0 = Karte erkannt und in Leseposition
             1 = Fehler
            -1 = Timeout
    '''

    if modus in [0, 1, 2]:
        txdata = b"C:" + bytes([modus + 0x30]) # Reader enabled
    else:
        print ("Fehler: Falscher ENABLE-Modus: {}".format (modus))
        return 1
    res = ict.sendICT (ser, txdata)
    if res == ict.ACK:
        print ("Warte auf Karte... ",end="")
        rxdata = ict.recvICT(ser)
        if rxdata[0]==b'P':
            print ("OK")
    else:
        print ("Fehler: ENABLE fehlgeschlagen.")
        return 1        
    
    cnt = int(timeout // ict.POLLWAIT)
    
    cardstatus = 1 # keine Karte
    while cardstatus and cnt:
        status = check_status(ser)
        if isinstance(status, tuple):
            if status[0] == 0 and status[1]==2: # Karte erkannt und in Position?
                cardstatus = 0
                print ("OK.\n")
            else:
                cnt -= 1
                sleep(ict.POLLWAIT)
        else:
            print ("\nFehler: Keine Antwort auf Statusabfrage!")
    if cnt: # noch Pollversuche übrig?
        if ict.DEBUG:
            print ("Karte in Position: {}".format (check_status(ser)))
        return cardstatus
    else:
        return -1 # Timeout


def ejectcard (ser, modus=0):
    '''
    Karte auswerfen.
    Modus = 0 : zur Kundenseite auswerfen
            1 : nach hinten einziehen
    Return: 0 : Auswurf erfolgreich
            1 : Fehler
    '''
    if modus in [0, 1]:
        txdata = b"C3" + bytes([modus+0x30]) # Karte auswerfen
    else:
        print ("Fehler: Falscher EJECT-Modus: {}".format (modus))
        return 1
    
    res = ict.sendICT (ser, txdata)
    if res == ict.ACK:
        rxdata = ict.recvICT(ser)
        if rxdata[0] == b'P':
            return 0
    return 1

    

def getalltracks (ser, tracklist):
    if ict.DEBUG:
        print ("Angeforderte Tracks: {}".format(tracklist))
    trackset = [] # Ergebnisliste Spurdaten
    for track in [1, 2, 3]:
        if tracklist[track-1] == 0x31: # Daten enthalten?
            trackdata = ict.read_magstripe(ser, track) # dann auslesen
            try: # und an Ergebnisliste anhängen
                trackset.append(trackdata[1])
            except: # kein Tuple erhalten, Lesefehler
                print ("Fehler {} beim Lesen Spur {}.".format(trackdata, track-1))
                trackset.append("")
        else:
            trackset.append("")
    return trackset