import requests
import json
from flask import Flask, request

access_token = "NzE3NmMyMmYtYjYxNS00NTBlLWE1ZGYtMmJhYjdiNzhlNDBmZjUwZWRjNWQtODk4_PF84_6121c98f-64c5-48a2-95f7" \
               "-6e1f074ad37f "
app = Flask(__name__)


def name(person_id):
    headers = {'Authorization': 'Bearer ' + access_token, 'content-type': 'application/json'}
    response = requests.get("https://api.ciscospark.com/v1/people/" + person_id, headers=headers)
    response = json.loads(response.text)
    return response["displayName"]


def get_text(text_id):
    headers = {'Authorization': 'Bearer ' + access_token, 'content-type': 'application/json'}
    response = requests.get("https://api.ciscospark.com/v1/messages/" + text_id, headers=headers)
    text = json.loads(response.text)
    return text['text']


def post_message(room_id, text):
    headers = {'Authorization': 'Bearer ' + access_token, 'content-type': 'application/json'}
    data = {'roomId': room_id, 'markdown': text}
    response = requests.post("https://api.ciscospark.com/v1/messages", json=data, headers=headers)
    return response.text


# Bot Functions
def bot_greets(room_id, person_id):
    post_message(room_id, "Hello " + name(person_id) + ", This Bot helps you find nearest Airport, Simply provide me "
                                                       " Name or co-ordinates of any place and I will return nearest "
                                                       "Airport details \n\n- **loc &lt;place&gt;**")


def bot_invalid(room_id):
    post_message(room_id, "Sorry I dint understand that")


def bot_loc(room_id, loc):
    post_message(room_id, loc + "Hello")


@app.route('/', methods=['POST'])
def main():
    json_data = request.json
    data = json_data['data']
    person_email = data['personEmail']
    if person_email == "testbot2.1@webex.bot":
        return "DONE"
    text_id = data['id']
    person_id = data['personId']
    room_id = data["roomId"]
    text = get_text(text_id)
    room_type = data["roomType"]
    if room_type == "group":
        text = text.strip("Test Bot 2.1")
    if text.lower() == "hi" or text.lower() == "hello":
        bot_greets(room_id, person_id)
    elif len(text) <= 4:
        bot_invalid(room_id)
    elif text[0].lower() == "l" and text[1].lower() == "o" and text[2].lower() == "c" and text[3] == " ":
        bot_loc(room_id, "loc")
    elif text[0].lower() == "c" and text[1].lower() == "o" and text[2].lower() == "r" and text[3] == " ":
        bot_cor(room_id, "loc")
    else:
        bot_invalid(room_id)

    return "True"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
