
import os
import sys
import json
import requests
from flask import Flask, request
from secret_sauce.models import predict_action
app = Flask(__name__)
@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200


@app.route('/', methods=['POST'])

def main():
    data = request.get_json()
    if data["object"] == "page":
        for entry in data["entry"]:
            for message_event in entry["messaging"]:
                if message_event.get("message"):
                    sender_id = message_event["sender"]["id"]
                    recipent_id = message_event["recipient"]["id"]
                    message_text = message_event["message"]["text"]
                    reply = process_msg(message_text)
                    send_message(sender_id,reply)

def process_msg(message_text):
    intent = predict_action(str(message_text))
    if intent != "none":
        pass #actions to be implemented in dsl.py
    else:
        pass #seqtoseq model for normal chat to be implemented
    return "hello"


def send_message(recipient_id, message_text):

    params = {"access_token": os.environ["PAGE_ACCESS_TOKEN"]}
    headers = {"Content-Type": "application/json"}
    data = json.dumps({"recipient": {"id": recipient_id},"message": {"text": message_text}})
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)


@app.route('/test')

def testmain():
    pass
    #test user interface to be implemented

if __name__ == '__main__':
    app.debug = True
    app.run()
