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
        print("Error in all_genres: {code}".format(code=all_category_data["error"]["status"]))
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
                                "Authorization":"Bearer {}".format(bearer)}).json()["tracks"]
        if response["items"] == []:#"error" in response:
            print("Error in scrape_list_data: ")
            continue
        response = response["items"][0]
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
        # print(recs)
        single_rec = random.choice(recs)
        return single_rec[0],single_rec[1]
