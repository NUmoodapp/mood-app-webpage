import requests
import random
import json


""" Query all genres seed data defined by Spotify """
def all_genres(bearer):
    query = "https://api.spotify.com/v1/recommendations/available-genre-seeds"
    response = requests.get(query,
                            headers={"Content-Type":"application/json",
                                    "Authorization":"Bearer {}".format(bearer)}).json()
    if "error" in response:
        print("Error in all_genres: {code}".format(code=response["error"]["status"]))
        return []
    else:
        available_genre_seeds = response["genres"]
        return available_genre_seeds


""" From a list of songs, return the Spotify ID data """
def scrape_list_data(song_list, bearer):
    song_id_list = []
    artists_id_list = []
    for song, artist in song_list:
        query = "https://api.spotify.com/v1/search?q=track:{track_name}%20artist:{artist_name}&type=track&limit=1".format(track_name=song,artist_name=artist)
        response = requests.get(query,
                                headers={"Content-Type":"application/json",
                                            "Authorization":"Bearer {}".format(bearer)}).json()
        if "tracks" not in response or response["tracks"]["items"] == []:#"error" in response:
            print("Song not found in scrape_list_data, song skipped: ",song)
            continue
        response = response["tracks"]["items"][0]
        song_id_list.append(response["id"])
        artists_id_list.append(response["artists"][0]["id"])
    return song_id_list, artists_id_list


""" Get a list of recommendations 
        Currently takes the first two tracks, first two artists, first genre as seed data (limit is 5)
        Randomly selects one song from the return list 
        Does not yet incorporate emotions
            - Need to map emotions to target values for recommendation parameters (valence, danceability, etc)
            - Also work out a better scheme for selecting seed values
"""
def get_recommendations(seed_tracks, seed_artists, target_emotions, bearer):
    seed_genres = all_genres(bearer)
    if len(seed_tracks) > 2:
        tracks = '%2C'.join(seed_tracks[:2])
    else:
        tracks = '%2C'.join(seed_tracks)
    
    if len(seed_artists) > 2:
        artists = '%2C'.join(seed_artists[:2])
    else:
        artists = '%2C'.join(seed_artists)

    if len(seed_genres) > 1:
        genres = '%2C'.join(seed_genres[:1])
    else:
        genres = '%2C'.join(seed_genres)
    query = "https://api.spotify.com/v1/recommendations?seed_artists={artists}&seed_genres={genres}&seed_tracks={tracks}".format(artists=artists,genres=genres,tracks=tracks)
    response = requests.get(query,
                            headers={"Content-Type":"application/json",
                                        "Authorization":"Bearer {}".format(bearer)}).json()
    if "error" not in response:
        recs = response["tracks"]
        for index, data in enumerate(recs):
            recs[index] = [data["id"],data["name"]]
        single_rec = random.choice(recs)
        return single_rec[0],single_rec[1]



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


""" Get best match from dictionary of track features to parameter values supplied.
        - Decide which parameters to pass into the function / make helper function in this file
        - Come up with a matching scheme, ie do we:
            - weight different parameters higher that others?
            - do we sum the differences for each value and choose the song with the smallest overall sum?
            - do we use some algorithmic matching software or just build our own scheme?
            - etc.
"""
def get_match(track_features, emotions, bearer):
    danceability_dist = {}
    energy_dist = {}
    valence_dist = {}
    total_dist = {}
    emotion = max(emotions,key=emotions.get)

    # If joy is dominant emotion, just use min dist to joy
    if emotion == 'joy':
        print("Using joy as dominant emotion, finding min dist of danceability to joy...")
        for track in track_features.keys():
            danceability_dist[track] = abs(track_features[track]['danceability'] - emotions['joy'])
        match_id = min(danceability_dist, key=danceability_dist.get)
        query = "https://api.spotify.com/v1/tracks/{id}".format(id=match_id)
        response = requests.get(query,
                                headers={"Content-Type":"application/json",
                                            "Authorization":"Bearer {}".format(bearer)}).json()
        match_name = response["name"]
        print("danceability_dist mapping: ",json.dumps(danceability_dist,indent=4))
        print("best match (min dist): ",match_id,":",match_name)
        return match_id, match_name

    # If no emotion is above 0.5, use the average of all the emotions as the energy
    if emotions[emotion] <= 0.5:
        print("Using average of all emotions, finding min dist of energy to avg...")
        energy = sum(emotions.values())/len(emotions.keys())
        for track in track_features.keys():
            energy_dist[track] = abs(track_features[track]['energy'] - energy)
        match_id = min(energy_dist, key=energy_dist.get)
        query = "https://api.spotify.com/v1/tracks/{id}".format(id=match_id)
        response = requests.get(query,
                                headers={"Content-Type":"application/json",
                                            "Authorization":"Bearer {}".format(bearer)}).json()
        match_name = response["name"]
        print("energy_dist mapping: ",json.dumps(energy_dist,indent=4))
        print("best match (min dist): ",match_id,":",match_name)
        return match_id, match_name

    # Else, use valence as the scale from joy to sadness
    print("Using scale from joy to sadness, finding min dist of valence to scale...")
    valence = abs(emotions['joy'] - emotions['sadness'])/2
    for track in track_features.keys():
        # If joy is dominant emotion, just use min dist to joy
        valence_dist[track] = abs(track_features[track]['valence'] - valence)
    match_id = min(valence_dist, key=valence_dist.get)
    query = "https://api.spotify.com/v1/tracks/{id}".format(id=match_id)
    response = requests.get(query,
                            headers={"Content-Type":"application/json",
                                        "Authorization":"Bearer {}".format(bearer)}).json()
    match_name = response["name"]
    print("valence_dist mapping: ",json.dumps(valence_dist,indent=4))
    print("best match (min dist): ",match_id,":",match_name)
    return match_id, match_name


