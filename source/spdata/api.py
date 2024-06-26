# gaining authorization for spotify api to query its datasets
from dotenv import load_dotenv
import os
import base64
from requests import post , get
import json
import pandas as pd

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

print(client_id, client_secret)

def get_token():
    auth_string = client_id + ":" + client_secret  # Correct the variable name here
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")
    
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type":"client_credentials"}
    result = post(url, headers=headers, data=data)
    
    # Print the status code and response content
    print("Status Code:", result.status_code)
    print("Response Content:", result.content)
    
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

def search_for_artists(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"

    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]
   
    if len(json_result) == 0:
        print("No artists with that name found")
        return None 

    return json_result[0]

def get_songs_by(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["tracks"]
    return json_result


def top_songs(artist):
    token = get_token()
    result = search_for_artists(token, artist)
    if not result:
        print(f"No artist found for {artist}")
        return []
    artist_id = result["id"]
    songs = get_songs_by(token, artist_id)
    
    final = []
    for idx, song in enumerate(songs):
        song_info = f"{idx + 1}. {song['name']}"
        final.append(song_info)
        print(song_info)  # If you still want to print the songs

    return final
