import sys
from flask import Flask, json, request
from flask_cors import CORS, cross_origin
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

MSG_BUFFFER = []

HOST = '127.0.0.1'
PORT = 33000

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
    send(msg)
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

def send(msg):  # implictly passed by binders.
    """Handles sending of messages."""
    CLIENT_SOCKET.send(bytes(msg, "utf8"))

if __name__ == '__main__':
    try:
        receive_thread = Thread(target=receive)
        receive_thread.start()
        api.run(debug=True, port=sys.argv[1])
    except IndexError:
        print('Port Please')