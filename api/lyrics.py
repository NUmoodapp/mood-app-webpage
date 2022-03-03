import requests
import urllib.request
import urllib.parse
import json
from bs4 import BeautifulSoup
import api_keys
import pprint 

### Search functions

base = "https://api.genius.com"
client_access_token = api_keys.my_client_access_token
token = 'Bearer {}'.format(client_access_token)
headers = {'Authorization': token}

def search(term):
    url = base + '/search'
    params = {'q': term}

    # url = "https://genius.com"
    page = requests.get(url, params = params, headers=headers)
    json = page.json()


    return json


def lookup_song(song_name, artist_name):
    json = search(song_name)

    for hit in json["response"]["hits"]:
        if hit["result"]["primary_artist"]["name"] == artist_name:
            song_info = hit
            break

    if song_info:
        song_api_path = song_info["result"]["api_path"]
        return song_api_path



def lyrics_from_song_api_path(song_api_path):
    song_url = base + song_api_path
  
    response = requests.get(song_url, headers=headers)
    json = response.json()
  
    path = json["response"]["song"]["path"]
    print(path)
    #gotta go regular html scraping... come on Genius
    page_url = "http://genius.com" + path
    page = requests.get(page_url)
    # html = BeautifulSoup(page.text, "html.parser")
    # # print(html)
    # lyrics = page.find("div", {"class": "lyrics"})
    # print(lyrics)

    soup = BeautifulSoup(page.content, 'html.parser')
    print(soup.find_all('p'))

    #remove script tags that they put in the middle of the lyrics
    # [h.extract() for h in html('script')]
    # print(html)
    #at least Genius is nice and has a tag called 'lyrics'!
    # lyrics = html.find("div", class_="lyrics").get_text() #updated css where the lyrics are based in HTML
    return


def main():
    # Example searches
    term = 'gooey'
    # artist_id = 72


    # Shows some random songs from arist and lyrics
    print(lyrics_from_song_api_path(lookup_song(term, 'Glass Animals')))


if __name__ == "__main__":
    main()




#### Tests

