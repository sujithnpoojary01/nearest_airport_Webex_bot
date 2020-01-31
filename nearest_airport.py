import requests
import json
from flask import Flask, request

access_token = "NzE3NmMyMmYtYjYxNS00NTBlLWE1ZGYtMmJhYjdiNzhlNDBmZjUwZWRjNWQtODk4_PF84_6121c98f-64c5-48a2-95f7" \
               "-6e1f074ad37f "
app = Flask(__name__)


def get_text(text_id):
    headers = {'Authorization': 'Bearer ' + access_token, 'content-type': 'application/json'}
    response = requests.get("https://api.ciscospark.com/v1/messages/"+text_id, headers=headers)
    text = json.loads(response.text)
    return text['text']


def post_message(room_id, text_id):
    headers = {'Authorization': 'Bearer ' + access_token, 'content-type': 'application/json'}
    data = {'roomId': room_id, 'text': get_text(text_id)}
    response = requests.post("https://api.ciscospark.com/v1/messages", json=data, headers=headers)
    return response.text


@app.route('/', methods=['POST'])
def main():
    json_data = request.json
    data = json_data['data']
    person_email = data['personEmail']
    if person_email == "testbot2.1@webex.bot":
        return "DONE"
    text_id = data['id']
    room_id = data["roomId"]
    return json.loads(post_message(room_id, text_id))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)

