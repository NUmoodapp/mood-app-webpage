import time
from flask import Flask, request
from IBMWatson import SentimentAnalysis
import json
import urllib.request
import re

app = Flask(__name__)

@app.route('/song', methods=['POST'])
def get_song():
    statement = request.get_json().get('statement')
    # right now, statement will hold exactly what Azure transcribed
    # i.e., if Watson does text cleaning, it should be implemented here
    SentimentAnalysis(statement)
    # right now, I just search youtube for the statement and return the id of the first video
    search_keywords = "+".join(statement.split())
    html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + search_keywords);
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
    if not video_ids:
        return {'song': ''}
    return {'song': [statement, "https://www.youtube.com/embed/" + video_ids[0]]}


