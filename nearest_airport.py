import os
import requests
import json
from flask import Flask, request

access_token = "Zjk3Y2I5OTAtZWEwZS00YzdkLTg5YTAtYzQ3YjFiM2NjY2JhNmRlMDFlNjItM2Rh_PF84_6121c98f-64c5-48a2-95f7-6e1f074ad37f"
app = Flask(__name__)


def name(person_id):
    headers = {'Authorization': 'Bearer ' + access_token, 'content-type': 'application/json'}
    response = requests.get("https://api.ciscospark.com/v1/people/" + person_id, headers=headers)
    response = json.loads(response.text)
    return response["nickName"]


def get_text(text_id):
    headers = {'Authorization': 'Bearer ' + access_token, 'content-type': 'application/json'}
    response = requests.get("https://api.ciscospark.com/v1/messages/" + text_id, headers=headers)
    text = json.loads(response.text)
    return text['text']


def post_message(room_id, text):
    headers = {'Authorization': 'Bearer ' + access_token, 'content-type': 'application/json'}
    data = {'roomId': room_id, 'markdown': text}
    response = requests.post("https://api.ciscospark.com/v1/messages", json=data, headers=headers)
    print(response)
    return response.text


# Bot Functions
def bot_greets(room_id, person_id):
    post_message(room_id, "Hello " + name(person_id) + ", I am a Demo Bot! I can help you find nearest Airport, Simply provide me "
                                                       "the name of any place and I will return nearest "
                                                       "Airport details \n\n- type **loc &lt;place&gt;** Example: **loc Hampi** or **loc Chandler, Arizona**")


def bot_invalid(room_id):
    post_message(room_id, "Sorry I dint understand that. Type **help** to see how I can assist you.")


def bot_loc(room_id, loc):
    try:
        url = "https://us1.locationiq.com/v1/search.php"

        data = {'key': '38811a440c2ff2','q': loc,'format': 'json'}

        response = requests.get(url, params=data)
        response = json.loads(response.text)
        lat = response[0]["lat"]
        lon = response[0]["lon"]
        dp = response[0]["display_name"]
        print(response)
        bot_cor(room_id, lon, lat, dp)
    except:
        print(loc) 
        post_message(room_id, "Could not find the place, try modiyfing the keyword or be more specific by adding the state/country of place as given below\n\n"+"**loc **"+loc+", **&lt;State/Country&gt;**")


def bot_cor(room_id, lon, lat, dp):
    link = "https://cometari-airportsfinder-v1.p.rapidapi.com/api/airports/nearest"

    data = {"lng": lon, "lat": lat}

    head = {
        'x-rapidapi-host': "cometari-airportsfinder-v1.p.rapidapi.com",
        'x-rapidapi-key': "a0ff15293cmsh90b4c227a309657p1fa429jsn1de1b4d95554"
    }

    res = requests.request("GET", link, headers=head, params=data)
    res = json.loads(res.text)
    code = res["code"]
    print(code)
    link = "https://airport-info.p.rapidapi.com/airport"

    data = {"iata": code}

    headers = {
        'x-rapidapi-host': "airport-info.p.rapidapi.com",
        'x-rapidapi-key': "0d9e22f3aamsh555874dd0c2b481p1b3244jsn430ecfb5fd9a"
    }

    response = requests.request("GET", link, headers=headers, params=data)
    print(response.text)

    response = json.loads(response.text)
    post_message(room_id, " **Place :**"+dp+"\n\n"+"**Nearest Airport :**"+response['name']+"\n\n"+"**Airport Code :**"+response['iata']+"\n\n"+"**Airport Location :**"+response["location"])


@app.route('/', methods=['POST'])
def main():
    json_data = request.json
    data = json_data['data']
    person_email = data['personEmail']
    if person_email == "nearest_airport@webex.bot":
        return "DONE"
    text_id = data['id']
    person_id = data['personId']
    room_id = data["roomId"]
    text = get_text(text_id)
    print(text)
    room_type = data["roomType"]
    if room_type == "group":
        if "Nearest Airport" in text:
            text = text.replace("Nearest Airport", "")
        elif "Nearest" in text:
            text = text.replace("Nearest", "")
    text = text.strip()
    print(text)
    if text.lower() == "hi" or text.lower() == "hello" or text.lower() == "help":
        bot_greets(room_id, person_id)
    elif len(text) <= 4:
        bot_invalid(room_id)
    elif text[0].lower() == "l" and text[1].lower() == "o" and text[2].lower() == "c" and text[3] == " ":
        text = text[4:]
        print(text)
        bot_loc(room_id, text)
    elif text[0].lower() == "c" and text[1].lower() == "o" and text[2].lower() == "r" and text[3] == " ":
        bot_loc(room_id, text)
    else:
        bot_invalid(room_id)

    return "True"



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
