#Functions for sending and receiving covert channels using scapy
#Code based off https://github.com/jeffreysasaki/covertchannel/blob/master/src/client.py

import sys
from scapy import all as scapy
pkt = None

#Send covert message
def sendCovert(dest, msg):
    msg += "\n"
    for char in msg:
        new_pkt = craft(char, dest)
        scapy.send(new_pkt)

# Craft the packet to send
def craft(character, dest):
    global pkt
    char = ord(character) # covert character to decimal value
    pkt=scapy.IP(dst=dest)/scapy.TCP(sport=char, dport=scapy.RandNum(0, 65535), flags="E")
    return pkt

# Listens and filter covert traffic, denoted with an "E" flag
def parse(pkt):
    flag=pkt['TCP'].flags
    if flag == 0x40:
        char = chr(pkt['TCP'].sport)
        sys.stdout.write(char)

# Sniff for packets meeting criteria of parse
def covertListen():
    scapy.sniff(filter="tcp", prn=parse)
