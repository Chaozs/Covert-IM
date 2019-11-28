from flask import Flask, json, request
from flask_cors import CORS, cross_origin

MSG_BUFFFER = []

api = Flask(__name__)
cors = CORS(api)
api.config['CORS_HEADERS'] = 'Content-Type'

@api.route('/chat/get', methods=['POST'])
def get_companies():
    req_data = request.get_json()
    covert = req_data.get('covert')
    uid = req_data.get('uid')
    find = False
    if MSG_BUFFFER:
        for idx, id_msg in enumerate(MSG_BUFFFER):
            if id_msg[0] != uid:
                msg = id_msg[1]
                find = True
                break
        if find:
            del MSG_BUFFFER[idx]
            find = False
        else:
            msg = ''
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
    MSG_BUFFFER.append((uid, msg))
    print(MSG_BUFFFER)
    return json.dumps({"success": True}), 201

if __name__ == '__main__':
    api.run(debug=True)