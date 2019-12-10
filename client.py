#Source code from: https://medium.com/swlh/lets-write-a-chat-app-in-python-f6783a9ac170
#!/usr/bin/env python3
"""Script for Tkinter GUI chat client."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter #python GUI bilding tool
from srcPortSpoof import sendCovert, covertListen
# import queue #For sharing information between threads.
import sys


numChannels = 2 #Number of different chat channels
mode = 0        #which chat channel
msg = ""
covertMsg = ""  #covert channel message

def receive():
    """Handles receiving of messages."""
    #infinite loop due to receiving messages non-deterministically
    while True:
        
        # This try is for handling covert messages.
        # try:
        #     covertMsg = msgQ.get(False)
        #     sys.stdout.write(covertMsg)
        #     msg_list.insert(tkinter.END, covertMsg)
        # except queue.Empty:
        #     pass

        # This Try is for handling public messages.
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            msg_list.insert(tkinter.END, msg)
        except OSError:  # Possibly client has left the chat.
            break



def send(event=None):  # implictly passed by binders.
    global mode
    global msg
    global HOST
    """Handles sending of messages."""
    msg = my_msg.get() #input field on GUI
    my_msg.set("")  # Clears input field.
    #Mode 0 = send regular message
    if mode == 0:
        client_socket.send(bytes(msg, "utf8"))
        if msg == "{quit}": #client is closed
            client_socket.close()
            top.quit()
    #Mode 1 = send message to covert channel #1
    if mode == 1:
        sendCovert(HOST, msg)

def swap(event=None):
    global mode
    global numChannel
    if mode == (numChannels - 1):
        mode = 0
        print (mode)
    else:
        mode = mode + 1
        print (mode)


def on_closing(event=None):
    """This function is to be called when the window is closed."""
    my_msg.set("{quit}")
    send()

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
#Swap button
switch_button = tkinter.Button(top, text="Swap", command=swap)
switch_button.pack()

top.protocol("WM_DELETE_WINDOW", on_closing)


#for connecting to server
#HOST = input('Enter host: ')
HOST = '127.0.0.1'
PORT = 33000
##PORT = input('Enter port: ')
##if not PORT:
##    PORT = 33000
##else:
##    PORT = int(PORT)

BUFSIZ = 1024
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target=receive)
receive_thread.start()

#Create thread for listening to covert channel, passing on a queue as reference.
covert_thread = Thread(target=covertListen, args=(msgQ,))
covert_thread.start()

tkinter.mainloop()  # Starts GUI execution.
