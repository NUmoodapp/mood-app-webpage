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
    for song in json_data["response"]["hits"]:
        print(song["result"]["full_title"])


# Use: get_song_list(search_genius("[search term]"))
