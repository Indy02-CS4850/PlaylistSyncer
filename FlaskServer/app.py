import json

import requests
import base64
from flask import Flask, request, jsonify
from flask_cors import CORS
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import applemusicpy

app = Flask(__name__)
CORS(app)

# read spotify client id from file
@app.route('/get_spotify_data', methods=['GET'])
def get_spotify_data():
    spotify_client_id = open("spotify_client_id.txt", "r").read()
    return jsonify({"spotify_client_id": spotify_client_id})

# read apple dev token from file
@app.route('/get_apple_data', methods=['GET'])
def get_apple_data():
    apple_dev_token = open("apple_dev_token.txt", "r").read()
    return jsonify({"apple_dev_token": apple_dev_token})

@app.route('/get_playlists_apple', methods=['POST'])
def get_playlists():
    try:
        # get passed data from flutter js
        received_data = request.get_json()
        apple_id_token = received_data.get("auth_key")
        # read apple dev token from file
        apple_dev_token = open("apple_dev_token.txt", "r").read()

        # Make a GET request to MusicKit API
        headers = {
            'Authorization': "Bearer " + apple_dev_token,
            'Music-User-Token': apple_id_token
        }
        response = requests.get("https://api.music.apple.com/v1/me/library/playlists", headers=headers)
        # if successful request return results (playlist names + ids) to flutter js
        if response.status_code == 200:
            playlists_data = response.json().get('data', [])
            playlists = [{'name': p['attributes']['name'], 'id': p['id']} for p in playlists_data]
            print(playlists)
            return jsonify(playlists)
        else:
            print(response.status_code)
            return jsonify({'error': 'Unable to fetch playlists'})
    except Exception as e:
        return jsonify({'error': str(e)})

# generate spotify access token based on client id, secret id, and user auth key
@app.route('/get_access_token_spotify', methods=['POST'])
def get_access_token_spotify():
    # get passed data from flutter js
    received_data = request.get_json()
    spotify_id_token = received_data.get("auth_key")
    # read spotify client id and secret id from file
    spotify_client_id = open("spotify_client_id.txt", "r").read()
    spotify_client_secret = open("spotify_client_secret.txt", "r").read()
    # encode credentials
    encoded_credentials = base64.b64encode(spotify_client_id.encode() + b':' + spotify_client_secret.encode()).decode("utf-8")

    # form data to send
    token_headers = {
        "Authorization": "Basic " + encoded_credentials,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    token_data = {
        "grant_type": "authorization_code",
        "code": spotify_id_token,
        "redirect_uri": "http://99.8.194.131:8000/"  # remember to change this when moving to prod
    }

    # get token from spotify and send back to flutter js
    r = requests.post("https://accounts.spotify.com/api/token", data=token_data, headers=token_headers)
    print(r.json())
    token = r.json()["access_token"]
    print(token)
    return jsonify({"access_token": token})


@app.route('/get_playlists_spotify', methods=['POST'])
def get_playlists_spotify():
    try:
        # Get the current user's playlists from passed data
        received_data = request.get_json()
        spotify_id_token = received_data.get("auth_key")

        # Set up headers and parameters for the request
        user_headers = {
            "Authorization": "Bearer " + spotify_id_token,
            "Content-Type": "application/json"
        }
        user_params = {
            "limit": 50
        }

        # get playlists from spotify
        user_playlists_response = requests.get("https://api.spotify.com/v1/me/playlists", params=user_params,
                                               headers=user_headers)
        # if successful request return results (playlist names + ids) to flutter js
        # Format the playlists
        formatted_playlists = []
        for playlist in user_playlists_response.json()['items']:
            playlist_id = playlist['id']
            playlist_name = playlist['name']

            # Add the playlist and its tracks to the list
            formatted_playlists.append({
                'id': playlist_id,
                'name': playlist_name
            })

        return jsonify(formatted_playlists)

    except spotipy.SpotifyException as e:
        return jsonify({'error': str(e)})


@app.route('/create_playlists_apple_music_to_spotify', methods=['POST'])
def create_playlists_apple_music_to_spotify():
    # get passed data from flutter js
    received_data = request.get_json()
    apple_id_token = received_data.get("apple_id_token")
    apple_playlist_id = received_data.get("apple_playlist_id")
    apple_playlist_name = received_data.get("apple_playlist_name")
    spotify_id_token = received_data.get("spotify_auth_key")

    # read apple dev token from file
    apple_dev_token = open("apple_dev_token.txt", "r").read()

    # Make a GET request to MusicKit API
    headers = {
        'Authorization': "Bearer " + apple_dev_token,
        'Music-User-Token': apple_id_token
    }
    apple_response = requests.get(
        "https://api.music.apple.com/v1/me/library/playlists/{}/tracks".format(apple_playlist_id),
        headers=headers)

    # generate list of tracks from playlist data
    songs = []
    if apple_response.status_code == 200:
        playlists_data = apple_response.json().get('data', [])
        # print(playlists_data)
        for track in playlists_data:
            track_name = track.get('attributes', {}).get('name', 'Unknown Track')
            artist_name = track.get('attributes', {}).get('artistName', 'Unknown Artist')
            album_name = track.get('attributes', {}).get('albumName', 'Unknown Album')
            songs.append({
                'track_name': track_name,
                'artist_name': artist_name,
                'album_name': album_name
            })
        print(songs)
    else:
        print(apple_response.status_code)
        return jsonify({'error': 'Unable to fetch playlists'})

    # create headers for spotify playlist creation request
    playlist_data = {
        "name": apple_playlist_name,
        "public": True  # Set to True for a public playlist, False for private
    }
    create_playlist_url = "https://api.spotify.com/v1/me/playlists"
    headers = {
        "Authorization": f"Bearer {spotify_id_token}",
        "Content-Type": "application/json"
    }
    # send request to Spotify to create a playlist
    response = requests.post(create_playlist_url, json=playlist_data, headers=headers)
    new_playlist_id = response.json()['id']  # get new playlist id to add songs
    for song in songs:
        try:
            # search for tracks on Spotify using name and artist name from Apple Music playlist
            song_search = song['track_name']
            song_artist = song['artist_name']
            search_query = f'{song_search} {song_artist}'
            search_url = f'https://api.spotify.com/v1/search?q={search_query}&type=track&limit=3'
            headers = {
                'Authorization': f'Bearer {spotify_id_token}',
                'Content-Type': 'application/json',
            }
            response = requests.get(search_url, headers=headers)
            found_song = response.json()['tracks']['items'][0]
            # add #1 found song to new generated Spotify playlist
            add_to_playlist_url = f'https://api.spotify.com/v1/playlists/{new_playlist_id}/tracks'
            track_uris = {"uris": [f'spotify:track:{found_song["id"]}'], "position": 0}
            response = requests.post(add_to_playlist_url, headers=headers, json=track_uris)
            if response.status_code == 200:
                print(f"Song with URI {found_song['id']} added to the playlist!")
            else:
                print(f"Error adding song to the playlist. Status code: {response.status_code}")

        except Exception as e:
            print("Failed to search")
            return jsonify({'error': str(e)})

    return {}


@app.route('/create_playlists_spotify_to_apple_music', methods=['POST'])
def create_playlists_spotify_to_apple_music():
    # get passed data from flutter js
    received_data = request.get_json()
    apple_id_token = received_data.get("apple_id_token")
    spotify_playlist_id = received_data.get("spotify_playlist_id")
    spotify_playlist_name = received_data.get("spotify_playlist_name")
    spotify_id_token = received_data.get("spotify_auth_key")

    # 1. query Apple Music for playlist
    apple_dev_token = open("apple_dev_token.txt", "r").read()

    # Define Apple Request headers
    apple_headers = {
        'Authorization': "Bearer " + apple_dev_token,
        'Music-User-Token': apple_id_token,
        'Content-Type': 'application/json'
    }

    # query spotify for playlist and return list of tracks in playlist
    songs = []
    user_headers = {
        "Authorization": "Bearer " + spotify_id_token,
        "Content-Type": "application/json"
    }
    spotify_playlist_get_response = requests.get(f"https://api.spotify.com/v1/playlists/{spotify_playlist_id}/tracks",
                                                 headers=user_headers)
    playlist_tracks = spotify_playlist_get_response.json()['items']

    # Format the found tracks
    formatted_tracks = []
    for track in playlist_tracks:
        track_name = track['track']['name']
        track_artist = track['track']['artists'][0]['name']
        formatted_tracks.append({
            'name': track_name,
            'artist': track_artist
        })

    # create data to populate Apple Track lists
    apple_songs = []
    apple_search_headers = {
        'Authorization': f'Bearer {apple_dev_token}',
    }

    # find and add all songs
    for track in formatted_tracks:
        # The song name goes here
        song_name = str(track.get('name')) + " " + str(track.get('artist'))
        song_name_encoded = requests.utils.quote(song_name)
        # search for song
        response = requests.get(
            f'https://api.music.apple.com/v1/catalog/us/search?types=songs&term={song_name_encoded}',
            headers=apple_search_headers)
        response_json = response.json()
        # Check if the request was successful, if so add song to apple_songs list
        if response.status_code == 200:
            song_to_add = response_json['results']['songs']['data'][0]
            apple_songs.append({"id": song_to_add['id'], "type": "songs"})
        else:
            print("Failed to get songs: ", response_json)

    # The new playlist details go here
    playlist_details = {
        "attributes": {
            "name": spotify_playlist_name,
            "description": "Generated Playlist from Spotify"
        },
        "relationships": {
            "tracks": {
                "data": apple_songs
            }
        }
    }
    # create new playlist with generated set of playlist ids
    apple_response = requests.post('https://api.music.apple.com/v1/me/library/playlists', headers=apple_headers,
                                   data=json.dumps(playlist_details))
    print(apple_response)
    return {}


if __name__ == '__main__':
    app.run(debug=True)
