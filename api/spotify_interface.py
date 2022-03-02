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


""" Get best match from dictionary of track features to parameter values supplied.
        - Basic shortest distance to ideal feature values for each track
        - Danceability is mapped directly to joy
        - Energy is mapped to the average of all the emotions -> Which will always be 0.5?
        - Valence is mapped to the scale of joy to sadness
        - Valence has a weight of 2, energy and danceability have weight of 1
        - All tracks are weighted by their confidence value passed from Genius
        - The track with the minimum overall distance is returned as the best match
"""
def get_match(track_features, track_confidences, emotions, bearer):
    total_dist = {}
    energy = sum(emotions.values())/len(emotions.keys())
    valence = abs(emotions['joy'] + emotions['sadness'])/2

    # Get Distance for all three values
    for track in track_features.keys():
        danceability_dist = abs(track_features[track]['danceability'] - emotions['joy'])
        energy_dist = abs(track_features[track]['energy'] - energy)
        valence_dist = abs(track_features[track]['valence'] - valence)
        total_dist[track] = (1-track_confidences[track])*(valence_dist + 2*energy_dist + 2*danceability_dist)

    match_id = min(total_dist, key=total_dist.get)
    query = "https://api.spotify.com/v1/tracks/{id}".format(id=match_id)
    response = requests.get(query,
                            headers={"Content-Type":"application/json",
                                        "Authorization":"Bearer {}".format(bearer)}).json()
    match_name = response["name"]
    print("total_dist mapping: ",json.dumps(total_dist,indent=4))
    print("best match (min dist): ",match_id,":",match_name)
    return match_id, match_name





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