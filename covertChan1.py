#Functions for sending and receiving covert channels using scapy
#Code based off https://github.com/jeffreysasaki/covertchannel/blob/master/src/client.py

import sys
from scapy import all as scapy
from scapy import *
#pkt = None
#testing commits

#Send covert message
def sendCovert(dest, msg):
        msg += "\n"
        temp_char_list = ["0","0","0","0"]
        i = 0
        src_ip = ""
        #print("Message to send is: "+msg)
        for char in msg:
        	if(i == 4):
                        #print("Temp list is: ")
                        #for t in temp_char_list:
                        #        print(t)
                        src_ip = spoof_IP(temp_char_list)
                        i=0
                        temp_char_list = ["*","*","*","*"]
                        temp_char_list[i] = char
                        i = i+1
                        new_pkt = craft(src_ip, dest)
                        scapy.send(new_pkt)
        	elif(char == "\n"):
        		temp_char_list[i] = char
        		i=i+1
        		src_ip = spoof_IP(temp_char_list)
        		new_pkt = craft(src_ip, dest)
        		scapy.send(new_pkt)
        	else:
                        temp_char_list[i] = char
                        i = i+1
        	
		
def spoof_IP(char_list):
        temp_ip = ""
        temp_ip = str(ord(char_list[0])) + "." + str(ord(char_list[1])) + "." + str(ord(char_list[2])) + "." + str(ord(char_list[3]))
        #print("Spoofed ip is: "+temp_ip)
        return temp_ip

# Craft the packet to send
def craft(spoofed_ip, dest):
	global pkt
        #char = ord(character) # covert character to decimal value
        #pkt=scapy.IP(dst=dest)/scapy.TCP(sport=char, dport=scapy.RandNum(0, 65535), flags="E")
	pkt=scapy.IP(src = spoofed_ip, dst=dest)/scapy.TCP(sport=scapy.RandNum(0, 65535), dport=scapy.RandNum(0, 65535), flags="E")
	#print("Packet IP is: " + pkt.src)
	return pkt

# Listens and filter covert traffic, denoted with an "E" flag
def parse(pkt):
    flag=pkt['TCP'].flags
    out = ""
    if flag == 0x40:
        ip = pkt['IP'].src
        #print("Message came from IP: " + ip)
        data = ip.split(".")
        char = [chr(int(data[0])), chr(int(data[1])), chr(int(data[2])), chr(int(data[3]))]
        for c in char:
                out+=c
        print("Message received was: " + out)

# Sniff for packets meeting criteria of parse
def covertListen():
    scapy.sniff(filter="tcp", prn=parse)
