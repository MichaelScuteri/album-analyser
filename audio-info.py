from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json
from collections import Counter
import urllib.parse

#-----------------------------------------------------------#
#--------------------------Get Auth-------------------------#
#-----------------------------------------------------------#

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

#Get access token
def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": f"Basic {auth_base64}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "client_credentials"
    }
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

#Create auth header for queries
def get_auth_header(token):
    return{"Authorization": f"Bearer {token}"}

#-----------------------------------------------------------#
#------------------------API Queries------------------------#
#-----------------------------------------------------------#

def get_album_id(token, album):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={album}&type=album&limit=1"

    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["albums"]["items"]
    if len(json_result) == 0:
        print(f"Could not find album with name")
        return None
    return json_result[0]

def get_album_info(token, album_id):
    url = f"https://api.spotify.com/v1/albums/{album_id}"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)
    tracks = json_result["tracks"]["items"]
    album_name = json_result["name"]
    if len(tracks) == 0:
        print(f"No songs found in the album")
        return None
    song_ids = [track.get("id") for track in tracks]
    return song_ids, album_name

def get_audio_info(token, song_ids):
    tempo = []
    duration_raw = []
    key_raw = []
    mode = []
    energy = []
    danceability = []
    happiness = []
    for song_id in song_ids:
        url = f"https://api.spotify.com/v1/audio-features/{song_id}"
        headers = get_auth_header(token)
        result = get(url, headers=headers)
        json_result = json.loads(result.content)
        tempo_raw =int(json_result["tempo"])
        tempo.append(tempo_raw)
        duration_raw.append(json_result["duration_ms"])
        key_raw.append(json_result["key"])
        mode.append(json_result["mode"])
        energy.append(json_result["energy"])
        danceability.append(json_result["danceability"])
        happiness.append(json_result["valence"])
    return tempo, duration_raw, key_raw, mode, energy, danceability, happiness

def get_song_id(token, song):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={song}&type=track&limit=1"

    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["tracks"]["items"]
    if len(json_result) == 0:
        print(f"Could not find track with name: {song}")
        return None
    return json_result[0]

def get_song_info(token, song_id):
    url = f"https://api.spotify.com/v1/tracks/{song_id}"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)
    return json_result

def get_artist_names(song_info):
    artists = song_info["artists"]
    artist_names = [artist["name"] for artist in artists]
    return ", ".join(artist_names)

def convert_duration(duration):
    durations = []
    for each in duration:
        total_seconds = each // 1000
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        durations.append(f"{minutes}:{seconds:02d}")

    total_duration = sum(duration)
    average_length_ms = total_duration // len(duration)
    average_seconds = average_length_ms // 1000
    average_minutes = average_seconds // 60
    average_seconds = average_seconds % 60
    
    return f"{average_minutes}:{average_seconds:02d}"

def convert_key_to_note(keys_raw):
    notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    keys = []
    for key in keys_raw:
        if keys == -1:
            return "No key data available"
        keys.append(notes[key])
    counter = Counter(keys)
    common_key, key_count = counter.most_common(1)[0]

    return ", ".join(keys), common_key, key_count

def main():
    #input and initial data collection
    #name = input("Enter song name: ")
    token = get_token()     
    album_id = get_album_id(token, "After Hours")
    song_ids, album_name = get_album_info(token, album_id["id"])
    tempo, duration_ms, keys_raw, mode, energy, danceability, happiness = get_audio_info(token, song_ids)

    #calculations and statistics
    tempo_avg = round(sum(tempo) / len(tempo))
    average_duration = convert_duration(duration_ms)
    keys, common_key, key_count = convert_key_to_note(keys_raw)

    #output results
    print(album_name)
    print(f"Most Common Key: {common_key} ({key_count} tracks)")
    print(f"Average BPM: {tempo_avg}")
    print(f"Average Track Length: {average_duration}")

if __name__ == "__main__":
    main()

