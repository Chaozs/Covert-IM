#Source code from: https://medium.com/swlh/lets-write-a-chat-app-in-python-f6783a9ac170
#!/usr/bin/env python3
"""Script for Tkinter GUI chat client."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from scapy.all import sniff
import tkinter #python GUI bilding tool
import sys


def receive():
    """Handles receiving of messages."""
    #infinite loop due to receiving messages non-deterministically
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            msg_list.insert(tkinter.END, msg)
        except OSError:  # Possibly client has left the chat.
            break


def send(event=None):  # implictly passed by binders.
    """Handles sending of messages."""
    msg = my_msg.get() #input field on GUI
    my_msg.set("")  # Clears input field.
    client_socket.send(bytes(msg, "utf8"))
    if msg == "{quit}": #client is closed
        client_socket.close()
        top.quit()


def on_closing(event=None):
    """This function is to be called when the window is closed."""
    my_msg.set("{quit}")
    send()

# Listens and filter covert traffic, denoted with an "E" flag
def parse(pkt):
    flag=pkt['TCP'].flags
    if flag == 0x40:
        char = chr(pkt['TCP'].sport)
        sys.stdout.write(char)

def covertListen():
    scapy.sniff(filter="tcp", prn=parse)

top = tkinter.Tk()
top.title("Chatter")

#frame for holding list of messages
messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()  # For the messages to be sent.
my_msg.set("Type your messages here.")
scrollbar = tkinter.Scrollbar(messages_frame)  # To navigate through past messages.

#message list which will be stored in messages_frame
# Following will contain the messages.
msg_list = tkinter.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()

#input field for user to input message
entry_field = tkinter.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tkinter.Button(top, text="Send", command=send)
send_button.pack()

top.protocol("WM_DELETE_WINDOW", on_closing)


#for connecting to server
HOST = input('Enter host: ')
PORT = input('Enter port: ')
if not PORT:
    PORT = 33000
else:
    PORT = int(PORT)

BUFSIZ = 1024
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target=receive)
receive_thread.start()

covert_thread = Thread(target=covertListen)
covert_thread.start()

tkinter.mainloop()  # Starts GUI execution.
