# coding=utf-8
'''
Created on 07.12.2018

@author: bert
'''

import ict3q8 as ict


def ict_reset (ser):
    '''
    Sendet RESET zum Leser
    
    for txdata in [b"C00", b"CK0"]:
        res = ict.sendICT (ser, txdata)
    '''    
        
    txdata = b"C0032400001000"
    res = ict.sendICT (ser, txdata)
    if res == ict.ACK:
        rxdata = ict.recvICT(ser)
        if rxdata[0]==0x50:
            return (0, rxdata[1:].decode())
        else:
            return (1, rxdata[1:].decode())
    else:
        return 1


def read_magstripe(ser, track):
    if track in [1, 2, 3]:
        txdata = b"C6" + bytes([track+0x30]) # Lesekommando aufbauen
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
    