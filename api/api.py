import time
from flask import Flask, request
from IBMWatson import SentimentAnalysis
import json
import urllib.request
import re
import api_keys
import requests

app = Flask(__name__)

@app.route('/song', methods=['POST'])
def get_song():
    statement = request.get_json().get('statement')
    # right now, statement will hold exactly what Azure transcribed
    # i.e., if Watson does text cleaning, it should be implemented here
    analysisResults = SentimentAnalysis(statement)
    if (analysisResults):
        print(analysisResults['emotion']['document']['emotion'])
    # Searches spotify for the statement input, if no song is found it defaults to tell them to try again, will do a better error handling later
    emotion = max(analysisResults['emotion']['document']['emotion'],key=analysisResults['emotion']['document']['emotion'].get)
    url = 'https://www.apitutor.org/spotify/simple/v1/search?q={track_name}&type=track&limit=1'.format(track_name=emotion)
    tracks = requests.get(url).json()
    if not tracks:
        url = 'https://www.apitutor.org/spotify/simple/v1/search?q={track_name}&type=track&limit=1'.format(track_name='try again')
        tracks = requests.get(url).json()
        statement = 'No song found :('
    link = "https://open.spotify.com/embed/track/{track_id}?utm_source=generator".format(track_id=tracks[0].get('id'))
    return {'song': [statement, link]}



# genius

client_access_token = api_keys.my_client_access_token


def search_genius(search_term):
    genius_search_url = f"http://api.genius.com/search?q={search_term}&access_token={client_access_token}"

    response = requests.get(genius_search_url)
    json_data = response.json()

    return json_data

def get_song_list(json_data): #input = output of search()
    for song in json_data["response"]["hits"]:
        print(song["result"]["full_title"])


# Use: get_song_list(search_genius("[search term]"))
