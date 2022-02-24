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
    energy = sum(emotions.values())/len(emotions.keys())
    valence = abs(emotions['joy'] + emotions['sadness'])/2

    # Get Distance for all three values
    for track in track_features.keys():
        danceability_dist[track] = abs(track_features[track]['danceability'] - emotions['joy'])
        energy_dist[track] = abs(track_features[track]['energy'] - energy)
        valence_dist[track] = abs(track_features[track]['valence'] - valence)
        total_dist[track] = valence_dist[track] + 2*energy_dist[track] + 2*danceability_dist[track]
    
    match_id = min(total_dist, key=total_dist.get)
    query = "https://api.spotify.com/v1/tracks/{id}".format(id=match_id)
    response = requests.get(query,
                            headers={"Content-Type":"application/json",
                                        "Authorization":"Bearer {}".format(bearer)}).json()
    match_name = response["name"]
    print("total_dist mapping: ",json.dumps(total_dist,indent=4))
    print("best match (min dist): ",match_id,":",match_name)
    return match_id, match_name


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