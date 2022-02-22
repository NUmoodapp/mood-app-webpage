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
def get_match(track_features, valence, bearer):
    # TO DO
    # Currently just returns the data for the first track in the dictionary passed in
    for track in track_features.keys():
        match_id = track
        query = "https://api.spotify.com/v1/tracks/{id}".format(id=match_id)
        response = requests.get(query,
                                headers={"Content-Type":"application/json",
                                            "Authorization":"Bearer {}".format(bearer)}).json()
        match_name = response["name"]
        return match_id, match_name


