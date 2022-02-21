import time
from flask import Flask, request
from IBMWatson import SentimentAnalysis
import json
import urllib.request
import re
import api_keys
import requests
import itertools

app = Flask(__name__)

@app.route('/song', methods=['POST'])
def get_song():
    statement = request.get_json().get('statement')
    # right now, statement will hold exactly what Azure transcribed
    # i.e., if Watson does text cleaning, it should be implemented here
    analysisResults = SentimentAnalysis(statement)
    if (analysisResults):
        print(analysisResults['emotion']['document']['emotion'])
    # right now, I just search youtube for the statement and return the id of the first video
    search_keywords = "+".join(statement.split())
    html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + search_keywords);
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
    if not video_ids:
        return {'song': ''}
    return {'song': [statement, "https://www.youtube.com/embed/" + video_ids[0]]}



# genius

client_access_token = api_keys.my_client_access_token


def search_genius(search_term):
    genius_search_url = f"http://api.genius.com/search?q={search_term}&access_token={client_access_token}"

    response = requests.get(genius_search_url)
    json_data = response.json()

    return json_data

def get_song_list(json_data): #input = output of search()
    song_list = []
    for song in json_data["response"]["hits"]:
        song_list.append(song["result"]["full_title"])
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
    


    for word_combo in combos:
        if word_combo.lower() not in stop_words: 
            song_list.append(get_song_list(search_genius(word_combo)))

    return song_list

#search combinations of keywords

# print(connect_genius('i am sad and i like legos and airplanes and basketball'))
# connect_genius('i am sad and i like legos and airplanes and basketball')

# combos = [[()], [('airplanes',), ('basketball',), ('legos',)], [('airplanes', 'basketball'), ('airplanes', 'legos'), ('basketball', 'legos')], [('airplanes', 'basketball', 'legos')]]
# print(strip_combos(combos))

print(get_song_list(search_genius("travel")))
