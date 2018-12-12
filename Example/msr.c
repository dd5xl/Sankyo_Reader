#
#include <stdio.h>

#define INIT 0x0000
#define POLY 0x1021

unsigned short calc_crc (unsigned short crc, unsigned short ch);
unsigned short GetCRC (unsigned char *p, unsigned short n);

unsigned short calc_crc (unsigned short crc, unsigned short ch)
{
    unsigned short i;
    ch <<= 8;
    for (i=8; i>0; i--)
    {
        if ((ch^crc) & 0x8000)
        {
            crc=(crc<<1)^POLY;
        }
        else
        {
            crc<<=1;
        }
    }
    return crc;
}

unsigned short GetCRC (unsigned char *p, unsigned short n)
{
    unsigned char ch;
    unsigned short i;
    unsigned short crc = INIT;
    
    for (i=0; i<n; i++)
    {
        ch=*p++;
        crc=calc_crc(crc, (unsigned short)ch);
    }
    return crc;
}

int main (void)
{
    unsigned char TransCommand[13] = {0xF2, 0x00, 0x08, 0x43, 0x30, 0x30, 0x33, 0x32, 0x34, 0x30, 0x30, 0x00, 0x00};
    unsigned short TextLength = 11;
    unsigned short crc;
    
    crc = GetCRC (TransCommand, TextLength);
    printf ("CRC: %d\n\n", crc);
    return 0;
}
        