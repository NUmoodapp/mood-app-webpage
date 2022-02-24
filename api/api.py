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

    # right now, statement will hold exactly what Azure transcribed
    # i.e., if Watson does text cleaning, it should be implemented here
    analysisResults = SentimentAnalysis(statement)
    if (analysisResults):
        print("analysisResults:",analysisResults['emotion']['document']['emotion'])

    # Searches spotify for the statement input, if no song is found it defaults to tell them to try again, will do a better error handling later
    emotion = max(analysisResults['emotion']['document']['emotion'],key=analysisResults['emotion']['document']['emotion'].get)

    print(all_categories(spotify_token))

    # Steps to get track features from genius results:
    songs = parse_songs(connect_genius(statement))
    tracks,artists = scrape_list_data(songs, spotify_token)
    features = get_track_features(tracks, spotify_token)
    best_song_id, best_song_name = get_match(features, analysisResults['emotion']['document']['emotion'], spotify_token)

    link = "https://open.spotify.com/embed/track/{track_id}?utm_source=generator".format(track_id=best_song_id)
    return {'song': [best_song_name, link]}



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


def parse_songs(data):
    song_list = []
    for song in data:
        split_song = song.split(' by ')
        song_list.append(split_song)
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

def flatten_list(_2d_list):
    flat_list = []
    # Iterate through the outer list
    for element in _2d_list:
        if type(element) is list:
            # If the element is of type list, iterate through the sublist
            for item in element:
                flat_list.append(item)
        else:
            flat_list.append(element)
    return flat_list



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
    return flatten_list(song_list)



# to do
# ------

#connect song list return from connect_genius to get_song function somehow.
#search for best song from the list?

# print(connect_genius("i like legos and airplanes and also I like food and videos"))

