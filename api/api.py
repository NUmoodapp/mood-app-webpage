from sqlite3 import connect
import time
from flask import Flask, request
from IBMWatson import SentimentAnalysis
import json
import urllib.request
import re
import api_keys
import requests
import itertools
from spotify_interface import *

app = Flask(__name__)

@app.route('/song', methods=['POST'])
def get_song():
    statement = request.get_json().get('statement')
    spotify_token = request.get_json().get('token')
    print("token: ",spotify_token)
    # right now, statement will hold exactly what Azure transcribed
    # i.e., if Watson does text cleaning, it should be implemented here
    analysisResults = SentimentAnalysis(statement)
    if (analysisResults):
        print("analysisResults:",analysisResults['emotion']['document']['emotion'])

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

def get_song_list(json_data, cutoff = False): #input = output of search()
    song_list = []
    for song in json_data["response"]["hits"]:
        song_list.append(song["result"]["full_title"])

    if cutoff: return song_list[0:3]
    return song_list


def get_song_list_parsed(json_data):
    song_list = []
    for song in json_data["response"]["hits"]:
        title = song["result"]["full_title"].split('by')[0]
        artist = song["result"]["artist_names"]
        song_list.append([title,artist])
    return song_list

# Use: get_song_list(search_genius("[search term]"))

def convertTuple(tup):
    str = ''
    for item in range(len(tup)):
        if item == 0:
            str = str + tup[item]
        else: 
            str = str + " " + tup[item]
    return str

def strip_combos(combos):
    ret = []
    for c in combos:
        if c!= [()]:
            for combo in c:
                ret.append(convertTuple(combo))

    return ret



stop_words = ['the', 'and', 'a', 'an']

def connect_genius(search_term): #rename
    song_list = []
    res = SentimentAnalysis(search_term)
    search_keywords = res['keywords']
    search_keywords_list = []
    for s in search_keywords:
        search_keywords_list.append(s['text'])
    # print(search_keywords_list)


    combos = []
    for r in range(len(search_keywords_list)+1):
        combinations_obj = itertools.combinations(search_keywords_list, r)
        combos.append(list(combinations_obj))


    combos = strip_combos(combos)
    
    if len(combos) > 6:
        cutoff = False #change if necessary?
        combos = combos[0:6]
    else:
        cutoff = False

    


    for word_combo in combos:
        if word_combo.lower() not in stop_words: 
            x = get_song_list(search_genius(word_combo), cutoff)
            # print(x)
            for song in range(len(x)):
                x[song] = x[song].replace('\xa0', " ")

            song_list.append(x)
            #make sure song list isn't too long
    return song_list



# to do
# ------

#connect song list return from connect_genius to get_song function somehow.
#search for best song from the list?

# print(connect_genius("i like legos and airplanes and also I like food and videos"))

