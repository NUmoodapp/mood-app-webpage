import time
from flask import Flask, request
from IBMWatson import SentimentAnalysis
import json
import urllib.request
import re
import api_keys
import requests
from spotify_interface import *

app = Flask(__name__)

@app.route('/song', methods=['POST'])
def get_song():
    statement = request.get_json().get('statement')
    spotify_token = request.get_json().get('token')
    # right now, statement will hold exactly what Azure transcribed
    # i.e., if Watson does text cleaning, it should be implemented here
    analysisResults = SentimentAnalysis(statement)
    if (analysisResults):
        print(analysisResults['emotion']['document']['emotion'])

    # Searches spotify for the statement input, if no song is found it defaults to tell them to try again, will do a better error handling later
    emotion = max(analysisResults['emotion']['document']['emotion'],key=analysisResults['emotion']['document']['emotion'].get)

    song_list = get_song_list_parsed(search_genius("[{emotion}]"))
    tracks,artists = scrape_list_data(song_list,spotify_token)
    song_id, name = get_recommendations(tracks,artists,emotion,spotify_token)
    # features  = get_track_features(tracks, spotify_token) -> Gets feature values for all tracks in list, returns a dictionary


    link = "https://open.spotify.com/embed/track/{track_id}?utm_source=generator".format(track_id=song_id)
    return {'song': [name, link]}



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


def get_song_list_parsed(json_data):
    song_list = []
    for song in json_data["response"]["hits"]:
        title = song["result"]["full_title"].split('by')[0]
        artist = song["result"]["artist_names"]
        song_list.append([title,artist])
    return song_list

# Use: get_song_list(search_genius("[search term]"))
