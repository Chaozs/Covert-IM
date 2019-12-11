#Functions for sending and receiving covert channels using scapy
#Code based off https://github.com/jeffreysasaki/covertchannel/blob/master/src/client.py

import sys
from scapy import all as scapy
# from queue import Queue # for use in storing messages between main thread and this one.

# cMsg = ""
# q = None

#Send covert message
def sendCovertPort(dest, msg):
    msg += "\n"
    for char in msg:
        new_pkt = craft(char, dest)
        scapy.send(new_pkt, verbose=False)

# Craft the packet to send
def craft(character, dest):
    global pkt
    char = ord(character) # covert character to decimal value
    pkt=scapy.IP(dst=dest)/scapy.TCP(sport=char, dport=scapy.RandNum(0, 65535), flags="P")
    return pkt

# Listens and filter covert traffic, denoted with an "E" flag
def parse(pkt):
    char = ""
    flag=pkt['TCP'].flags
    # Not sure if this will work...
    if flag == "P":
        char = chr(pkt['TCP'].sport)
        sys.stdout.write(char) # Currently writing to console...
        sys.stdout.flush()

# Sniff for packets meeting criteria of parse
def covertListenPort():
    scapy.sniff(filter="tcp", prn=parse)
