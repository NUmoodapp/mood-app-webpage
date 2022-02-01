import time
from flask import Flask, request
import json

app = Flask(__name__)

@app.route('/song', methods=['POST'])
def get_song():
    statement = request.get_json().get('statement')
    # right now, statement will hold exactly what Azure transcribed
    # i.e., if Watson does text cleaning, it should be implemented here

    # right now, I'm just setting the song to the statement in all caps
    # and the spotify embed is hardcoded as Breezeblocks lol
    # replace this with song finding algo
    song = statement.upper()

    return {'song': song}