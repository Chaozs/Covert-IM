import sys
from flask import Flask, json, request
from flask_cors import CORS, cross_origin
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
# Files for our services. 
from srcPortSpoof import sendCovertPort, covertListenPort #as sendPort, portListen
from srcIPSpoof import sendCovertIP, covertListenIP #as sendIP, ipListen

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

MSG_BUFFFER = []

HOST = '127.0.0.1'
PORT = input('Enter port: ')
if not PORT:
    PORT = 33000
else:
    PORT = int(PORT)

BUFSIZ = 1024
ADDR = (HOST, PORT)

CLIENT_SOCKET = socket(AF_INET, SOCK_STREAM)
CLIENT_SOCKET.connect(ADDR)

api = Flask(__name__)
cors = CORS(api)
api.config['CORS_HEADERS'] = 'Content-Type'

@api.route('/chat/get', methods=['POST'])
def get_companies():
    req_data = request.get_json()
    covert = req_data.get('covert')
    # uid = req_data.get('uid')
    find = False
    if MSG_BUFFFER:
        msg = MSG_BUFFFER[-1]
        del MSG_BUFFFER[-1]
    else:
        msg = ''
    return json.dumps({
        "body": msg
        }), 200

@api.route('/chat/post', methods=['POST'])
def post_companies():
    req_data = request.get_json()
    covert = req_data.get('covert')
    uid = req_data.get('uid')
    msg = req_data.get('msg')
    if msg == "{quit}": #client is closed
        CLIENT_SOCKET.close()
    # MSG_BUFFFER.append((uid, msg))
    send(covert, msg)
    return json.dumps({"success": True}), 201

def receive():
    """Handles receiving of messages."""
    #infinite loop due to receiving messages non-deterministically
    while True:
        try:
            msg = CLIENT_SOCKET.recv(BUFSIZ).decode("utf8")
            MSG_BUFFFER.append(msg)
        except OSError:  # Possibly client has left the chat.
            break

def send(covert, msg):  # implictly passed by binders.
    """Handles sending of messages."""
    global HOST
    #Send regular message
    if covert == 'Normal':
        CLIENT_SOCKET.send(bytes(msg, "utf8"))
    #Send message through IP Spoof covert channel
    elif covert == 'IP SPOOF':
        sendCovertIP(HOST, msg)
    #Send message through IP Port covert Channel
    else:
        sendCovertPort(HOST, msg)

if __name__ == '__main__':
    try:
        receive_thread = Thread(target=receive)
        receive_thread.start()


        #Create thread for listening to covert channel
        covert_thread_port = Thread(target=covertListenPort)
        covert_thread_port.start()

        covert_thread_IP = Thread(target=covertListenIP)
        covert_thread_IP.start()
        
        api.run(port=sys.argv[1])
    except IndexError:
        print('Port Please')
