from sqlite3 import connect
import time
from flask import Flask, request, Response
from IBMWatson import SentimentAnalysis
import json
import urllib.request
import re
import api_keys
import requests
import itertools
from spotify_interface import *
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
from nltk.tokenize import word_tokenize

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

    song_conf = connect_genius(statement) #-> returns [[song by artist, confidence],...]
    songs = parse_songs(song_conf) #-> returns [[song, artist, confidence]]
    tracks, artists, confidences = scrape_list_data(songs, spotify_token)
    features = get_track_features(tracks, spotify_token)
    best_song_id, best_song_name = get_match(features, confidences, analysisResults['emotion']['document']['emotion'], spotify_token)
    if best_song_id is None:
        return {'song': [False, False]}
    link = "https://open.spotify.com/embed/track/{track_id}?utm_source=generator".format(track_id=best_song_id)
    return {'song': [best_song_name, link]}


def parse_songs(data):
    song_list = []
    for song_data in data:
        split_song = song_data[0].split(' by ')
        split_song.append(song_data[1])
        song_list.append(split_song)
    return song_list

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
    #get sentiment analysis results
    res = SentimentAnalysis(search_term)
    search_keywords = res['keywords']

    #print("Got keywords: ")
    #print(search_keywords)
    search_keywords_confidence_list = []
    
    #build list of search keywords from sentiment analysis
    search_keywords_list = []
    for s in search_keywords:
        words = s['text'].split(' ')
        search_keywords_list.extend(words)
        for word in words: 
            search_keywords_confidence_list.append([word, s['relevance']])

    print('keywords: ')
    print(search_keywords_list)
   
    #build list of all combinations of search keywords
    combos = []
    for r in range(len(search_keywords_list)+1):
        combinations_obj = itertools.combinations(search_keywords_list, len(search_keywords_list)+1 - r)
        combos.append(list(combinations_obj))

    combos = strip_combos(combos)
 
    

    #pair relevances
    for c in range(len(combos)):
        rlvnce = 0
        offset = 0
        for sw in search_keywords_confidence_list:
            if sw[0] in combos[c]:
                rlvnce += sw[1]
                offset += 1
        combos[c] = [combos[c], rlvnce/offset]



    for combo in combos:
        if combo[0].lower() not in stop_words: 
            x = get_song_list(search_genius(combo[0]))
            for song in range(len(x)):
                x[song] = x[song].replace('\xa0', " ")
                x[song] = [x[song], combo[1]]

            song_list.append(x)
            if len(flatten_list(song_list)) > 20:
                return flatten_list(song_list)
            
          
    return flatten_list(song_list)





