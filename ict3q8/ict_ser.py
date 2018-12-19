# coding=utf-8
'''
Created on 06.12.2018

@author: bert
'''

from ict3q8.ict_defs import *
from time import sleep
import serial
import struct


def checkCRC (dbuf):
    msb = 0 # 16-bit Startwert, 0x0000 = XModem
    lsb = 0
    for byte in dbuf:
        x = byte ^ msb
        x ^= (x >> 4)
        msb = (lsb ^(x >> 3) ^ (x << 4)) & 0xFF
        lsb = (x ^ (x << 5)) & 0xFF
    return (msb << 8) + lsb


def openCOM ():
    ser = serial.Serial(COMPORT, COMSPEED, timeout=COMTIMEOUT, bytesize=8, parity=serial.PARITY_EVEN, rtscts=1)
    return ser


def closeCOM (ser):
    ser.flush()
    return ser.close()
    

def sendICT (ser, txdata):
    
    if txdata:
        ackflag = NAK
        retries = COMRETRIES

        slen = len(txdata) # Länge der Nutzlast
        txbuf = STX_B + struct.pack (">H", slen) + txdata # STX + 2-Byte Länge + Nutzlast
        crc16 = checkCRC (txbuf) 
        txbuf += struct.pack(">H", crc16)

        while ackflag == NAK and retries:
            retries -= 1
            res = ser.write (txbuf)
            if DEBUG:
                print ("TX: {},   bytes sent: {},   Resp: ".format (txdata.decode(), res), end="")
            rxbuf = ser.read(1)
            if rxbuf:
                if rxbuf[0] in [ACK, NAK, DLE, EOT]:
                    ackflag = rxbuf[0]
                else:
                    print ("\nError: Invalid ACK byte received: {:2X}".format (rxbuf[0]))
            else:
                print ("\nError: no answer from ICT.")
            if ackflag == NAK:
                print ("NAK")
                sleep (NAKWAIT)
            elif ackflag == ACK and DEBUG:
                print ("ACK")
            elif ackflag == EOT:
                print ("EOT")
            elif ackflag == DLE:
                print ("DLE")
        
        return ackflag
    else:
        return 0
    
    
def recvICT (ser):
    nakcnt = COMRETRIES
    retrcnt = COMRETRIES
    nak = 1 # noch nichts gültiges empfangen
    while nak and nakcnt:
        crcbuf = ser.read(1) # Puffer für spätere CRC-Berechnung
        while crcbuf != STX_B and retrcnt:
            sleep (COMTIMEOUT)
            retrcnt -= 1
            crcbuf = ser.read(1)
        if retrcnt == 0: # nach cnt Versuchen kein STX empfangen
            return -1
        else: # retrcnt noch gültig, also wurde STX empfangen
            rxbuf = ser.read(2) # jetzt Länge lesen
            rxlen = struct.unpack(">H", rxbuf)[0]
            if rxlen < BUFLEN:
                crcbuf += rxbuf # geht auch in CRC ein
                rxbuf = ser.read(rxlen+2)
                crcbuf += rxbuf
                nak = checkCRC(crcbuf)
                if nak: 
                    print ("CRC-Fehler!")
                    nakcnt -= 1
                    ser.write(bytes([NAK]))
            else:
                print ("Empfangspuffer zu lang: {}". format (rxlen))
                nakcnt -= 1
                ser.write(bytes([NAK]))
    if nakcnt: # nakcnt noch gültig, also Daten empfangen
        return rxbuf[:-2] # CRC abtrennen
    else:
        return -1
    
    
def sendrecvICT (ser, txdata):
    res = sendICT(ser, txdata)
    resp = []
    if res == ACK:
        rxdata = recvICT(ser)
        if rxdata[0] == 0x50: # "P"
            resp.append(0)
            resp.append(rxdata[3]-0x30)
            resp.append(rxdata[4]-0x30)
            if len(rxdata)>5:
                resp.append(rxdata[5:])
        else:
            print(rxdata)
            resp.append(1)
            resp.append(rxdata[3]-0x30)
            resp.append(rxdata[4]-0x30)
    return resp    
