efawefawefewfew#Functions for sending and receiving covert channels using scapy
#Code based off https://github.com/jeffreysasaki/covertchannel/blob/master/src/client.py

import sys
from scapy import all as scapy
from scapy import *
#pkt = None
#testing commits

#Send covert message
def sendCovertIP(dest, msg):
        msg += "\n"
        temp_char_list = ["\0","\0","\0","\0"]
        i = 0
        src_ip = ""
        #This loop goes through the incoming string ofr encoding and break it up into lists of 4 chars to be
        #sent crafted into a fake IP
        for char in msg:
        	if(i == 4):
                        src_ip = spoof_IP(temp_char_list)
                        i=0
                        temp_char_list = ["\0","\0","\0","\0"]
                        temp_char_list[i] = char
                        i = i+1
                        new_pkt = craft(src_ip, dest)
                        scapy.send(new_pkt, verbose = False)
        	elif(char == "\n"):
        		temp_char_list[i] = char
        		i=i+1
        		src_ip = spoof_IP(temp_char_list)
        		new_pkt = craft(src_ip, dest)
        		scapy.send(new_pkt, verbose = False)
        	else:
                        temp_char_list[i] = char
                        i = i+1
        	
#This function receives a list of chars and converts them to ascii code before making a string to be used as an IP
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
        sys.stdout.write(out)
        sys.stdout.flush()

# Sniff for packets meeting criteria of parse
def covertListenIP():
    scapy.sniff(filter="tcp", prn=parse)
