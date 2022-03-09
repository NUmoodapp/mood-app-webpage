import requests
import random
import json


""" From a list of songs, return the Spotify ID data """
def scrape_list_data(song_list, bearer):
    song_id_list = []
    artists_id_list = []
    song_confidence_dict = {}
    for song, artist, confidence in song_list:
        query = "https://api.spotify.com/v1/search?q=track:{track_name}%20artist:{artist_name}&type=track&limit=1".format(track_name=song,artist_name=artist)
        response = requests.get(query,
                                headers={"Content-Type":"application/json",
                                            "Authorization":"Bearer {}".format(bearer)}).json()
        if "tracks" not in response or response["tracks"]["items"] == []:
            print("Song not found in scrape_list_data, song skipped: ",song," by ",artist)
            continue
        response = response["tracks"]["items"][0]
        song_id_list.append(response["id"])
        artists_id_list.append(response["artists"][0]["id"])
        song_confidence_dict[response["id"]] = confidence
        print("Adding ", song , " by ",artist," to list data")
    return song_id_list, artists_id_list, song_confidence_dict



""" Get audio features for a list of tracks, map them in dictionary to return """
def get_track_features(tracks, bearer):
    features = {}
    for track_id in tracks:
        query = "https://api.spotify.com/v1/audio-features/{id}".format(id=track_id)
        response = requests.get(query,
                                headers={"Content-Type":"application/json",
                                            "Authorization":"Bearer {}".format(bearer)}).json()
        features[track_id] = response
    return features


"""
Based on research from https://sites.tufts.edu/eeseniordesignhandbook/2015/music-mood-classification/
Faster tempo -> high energy
slower tempo -> lower energy, sad songs
loudness/intensity -> anger
softer -> suggests tenderness, sadness, or fear
high pitch -> happy, carefree, light moods
lower pitch -> dark, sad, serious mood

valence -> 0:1; positiveness, high = happy, low = negative (sad, depressed, angry)
tempo -> BPM, need to normalize; high = energetic, low = sad
speechiness -> above 0.66 is likely all spoken, throw these out
loudness -> -60:0db, need to normalize; high = anger, low = sadness or fear
key -> maps to pitch, -1 = none detected, 0:11; high = happy, low = sad
"""

def get_match(track_features, track_confidences, emotions, bearer):
    total_dist = {}
    sadness = {}
    joy = {}
    fear = {}
    anger = {}
    # Get distances for the emotions we care about for each track
    for track in track_features.keys():
        # If track is spoken, skip it  entirely
        if track_features[track]['speechiness'] > 0.66: continue

        # Normalize loudness, key, tempo (to out of 120 BPM)
        loudness = abs((track_features[track]['loudness']/60))
        key = track_features[track]['key']/11 if track_features[track]['key'] != -1 else 5/11
        tempo = track_features[track]['tempo']/180
        # Pull valence for time complexity (negligible prob but it looks nicer)
        valence = track_features[track]['valence']

        # Sadness ideals: valence 0, tempo 0, loudness 0, key 0
        sadness[track] = (abs(valence - 0) + abs(tempo - 0) + abs(loudness - 0)  + track_features[track]['danceability'])/4
        # Joy ideals: valence 1, tempo 1, key 1
        joy[track]= (abs(valence - 1) + abs(tempo - 1) + abs(key - 1) + abs(track_features[track]['danceability'] - 1))/4
        # Fear ideals: loudness 0
        fear[track] = abs(loudness - 0)
        # Anger ideals: valence 0, tempo 1, loudness 1
        anger[track]= (valence + (1 - track_features[track]['energy']) + (1 - tempo) + (1 - loudness))/4

        # Sum of all, weighted by confidence (1 - confidence since want the minimum dist)
        # Max emotion distance is weighted double, (everything else scaled by 2)
        total_dist[track] = (1 - track_confidences[track]) * (abs(emotions['sadness'] - sadness[track]) + 
                                                                abs(emotions['joy'] - joy[track]) + 
                                                                abs(emotions['fear'] - fear[track]) + 
                                                                abs(emotions['anger'] - anger[track]))

    if len(total_dist.keys()) == 0:
        print("No songs found.")
        return None, None

    max_emotion = max(emotions, key=emotions.get)
    if(emotions[max_emotion]>0.8):
        if(max_emotion == 'anger'): match_id = min(anger, key=anger.get)
        elif(max_emotion == 'joy'): match_id = min(joy, key=joy.get)
        elif(max_emotion == 'sadness'): match_id = min(sadness, key=sadness.get)
        elif(max_emotion == 'fear'): match_id = min(fear, key=fear.get)
        else: match_id = min(total_dist, key=total_dist.get)
    else:
        match_id = min(total_dist, key=total_dist.get)
        
    query = "https://api.spotify.com/v1/tracks/{id}".format(id=match_id)
    response = requests.get(query,
                            headers={"Content-Type":"application/json",
                                        "Authorization":"Bearer {}".format(bearer)}).json()
    match_name = response["name"]

    return match_id, match_name


# Old match function; can be deleted if new function is preferred
""" Get best match from dictionary of track features to parameter values supplied.
        - Basic shortest distance to ideal feature values for each track
        - Danceability is mapped directly to joy
        - Energy is mapped to the average of all the emotions -> Which will always be 0.5?
        - Valence is mapped to the scale of joy to sadness
        - Valence has a weight of 2, energy and danceability have weight of 1
        - All tracks are weighted by their confidence value passed from Genius
        - The track with the minimum overall distance is returned as the best match
"""
# def get_match(track_features, track_confidences, emotions, bearer):
#     total_dist = {}
#     energy = sum(emotions.values())/len(emotions.keys())
#     valence = abs(emotions['joy'] + emotions['sadness'])/2
#     valence = emotions['joy']

#     # Get Distance for all three values
#     for track in track_features.keys():
#         danceability_dist = abs(track_features[track]['danceability'] - emotions['joy'])
#         energy_dist = abs(track_features[track]['energy'] - energy)
#         valence_dist = abs(track_features[track]['valence'] - valence)
#         total_dist[track] = (1-track_confidences[track])*(valence_dist + 2*energy_dist + 2*danceability_dist)

#     match_id = min(total_dist, key=total_dist.get)
#     query = "https://api.spotify.com/v1/tracks/{id}".format(id=match_id)
#     response = requests.get(query,
#                             headers={"Content-Type":"application/json",
#                                         "Authorization":"Bearer {}".format(bearer)}).json()
#     match_name = response["name"]
#     print("total_dist mapping: ",json.dumps(total_dist,indent=4))
#     print("best match (min dist): ",match_id,":",match_name)
#     return match_id, match_name





# Functions to use in the event of no topic, can query songs from Spotify-made playlists.


""" Query all category ids defined by spotify """
def all_categories(bearer):
    query = "https://api.spotify.com/v1/browse/categories"
    all_category_data = requests.get(query,
                            headers={"Content-Type":"application/json",
                                    "Authorization":"Bearer {}".format(bearer)}).json()
    if "error" in all_category_data:
        print("Error in all_categories: {code}".format(code=all_category_data["error"]["status"]))
        return []
    else:
        data_items = all_category_data["categories"]["items"]
        ids = []
        for item in data_items:
            ids.append(item["id"])
        return ids



""" From a category id, get all playlists under that id """
def query_playlist_ids(category_id, bearer):
    query = "https://api.spotify.com/v1/browse/categories/{category_id}/playlists".format(category_id=category_id)
    response = requests.get(query,
                    headers={"Content-Type":"application/json",
                                "Authorization":"Bearer {}".format(bearer)}).json()
    if "error" in response:
        print("Error in query_playlist_ids: {code}".format(code=all_category_data["error"]["status"]))
        return []
    else:
        data_items = response["playlists"]["items"]
        playlist_ids = []
        for item in data_items:
            playlist_ids.append(item["id"])
        return playlist_ids



""" From a single playlist id, get all [track_id], [artist_id] in playlist """
def scrape_playlist_data(playlist_id, bearer):
    query = "https://api.spotify.com/v1/playlists/{playlist_id}/tracks".format(playlist_id=playlist_id)
    response = requests.get(query,
                    headers={"Content-Type":"application/json",
                                "Authorization":"Bearer {}".format(bearer)}).json()
    if "error" in response:
        print("Error in scrape_playlist_data: {code}".format(code=all_category_data["error"]["status"]))
        return []
    else:
        data_items = response["items"]
        track_data = []
        artist_data = []
        for item in data_items:
            if item["track"] is not None:
                track_data.append(item["track"]["id"])
                artist_data.append(item["track"]["artists"][0]["id"])
        return track_data, artist_data


""" From a list of playlist ids, data from each, return lists [tracks], [artists] """
def all_playlist_data(playlist_id_list, bearer):
    all_tracks = []
    all_artists = []
    for id in playlist_id_list:
        tracks, artists = scrape_playlist_data(id, bearer)
        for track in tracks:
            all_tracks.append(track)
        for artist in artists:
            all_artists.append(artist)
    return all_tracks, all_artists