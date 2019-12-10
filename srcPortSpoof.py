#Functions for sending and receiving covert channels using scapy
#Code based off https://github.com/jeffreysasaki/covertchannel/blob/master/src/client.py

import sys
from scapy import all as scapy
# from queue import Queue # for use in storing messages between main thread and this one.

# cMsg = ""
# q = None

#Send covert message
def sendCovert(dest, msg):
    msg += "\n"
    for char in msg:
        new_pkt = craft(char, dest)
        scapy.send(new_pkt, verbose=False)

# Craft the packet to send
def craft(character, dest):
    global pkt
    char = ord(character) # covert character to decimal value
    pkt=scapy.IP(dst=dest)/scapy.TCP(sport=char, dport=scapy.RandNum(0, 65535), flags="E")
    return pkt

# Listens and filter covert traffic, denoted with an "E" flag
def parse(pkt):
    char = ""
    flag=pkt['TCP'].flags
    if flag == 0x40:
        char = chr(pkt['TCP'].sport)
        sys.stdout.write(char) # Currently writing to console...

# def parsinig(pkt):
#     char = ""
#     flag=pkt['TCP'].flags
#     if flag == 0x40:
#         char = chr(pkt['TCP'].sport)
        # sys.stdout.write(char) # Currently writing to console...

# Sniff for packets meeting criteria of parse
def covertListen(refQ):
    # cMsg = ""
    # while True:
    #     pktLst = scapy.sniff(filter="tcp", prn=parsinig, count=20)
    #     pkt = pktLst[0]
    #     # sys.stdout.write(pkt[scapy.IP].src)
    #     flag = pkt[scapy.TCP].flags

    #     if flag == 0x40:
    #         try:
    #             char = chr(pkt[scapy.TCP].sport)
    #             # sys.stdout.write(char)
    #             if char == "\n":
    #                 refQ.put(cMsg)
    #                 cMsg = ""
    #             else:
    #                 cMsg += char
    #         except Exception as e:
    #             sys.stdout.write("Something went wrong...\n")
    #     else:
    #         sys.stdout.write("No Packets")
    scapy.sniff(filter="tcp", prn=parse)
