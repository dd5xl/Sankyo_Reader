# coding=utf-8
'''
Created on 06.12.2018

@author: bert
'''

# Debug switch
DEBUG=0


# COMM control
COMPORT = "/dev/ttyUSB0"
COMSPEED = 38400
COMTIMEOUT = 1 #(s)
COMRETRIES = 5
BUFLEN = 1019 # (1024 - 3 Header - 2 CRC)

# Timeouts
CARDINTIMER = 10 # (s) Wartezeit für Karte stecken 


# Protocol timing
NAKWAIT = 2 # (s)
POLLWAIT = 0.2

# Protocol control bytes
STX = 0xF2
ACK = 0x06
NAK = 0x15
EOT = 0x04
DLE = 0x10
STX_B = bytes([STX])
