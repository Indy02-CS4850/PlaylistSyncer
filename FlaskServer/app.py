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


# dev_token = "eyJhbGciOiJFUzI1NiIsImlzcyI6IlE2VEdZNUQ3TTIiLCJraWQiOiI2QlREQzdUTEJWIiwidHlwIjoiSldUIn0.eyJpc3MiOiI2OWE2ZGU5NS0wMjNmLTQ3ZTMtZTA1My0xMmxqbGVpbzNrYWp2emJ2IiwiaWF0IjoxNzExNzAwODgxLCJleHAiOjE3MTE3MDIwMjEsImF1ZCI6ImFwcHN0b3JlY29ubmVjdC12MSJ9.l3McweqdZ_EGV50vZue__cYVrZtyMB1rchbV4lUHFd_4BnTqUoLP0Qy9U_PmNdCncFeQQnfq-oj2QXS5RAQZHQ"
def get_user_playlists(user_apple_id_token):
    try:
        # Validate the Apple ID token (you can use pyjwt or any other library)
        # ...
        dev_token = "eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlE2VEdZNUQ3TTIifQ.eyJpYXQiOjE3MTE1MzI0MjUsImV4cCI6MTcyNzA4NDQyNSwiaXNzIjoiNkJUREM3VExCViJ9.jpq9oDEOCDiv9CiZKLkU8jfD8lLxUvooeI2fcat4hHlMr9nOv69jYhuAMNzimB4fHXGUFKOO0Mxtjv_SaFCQeQ"

        print(user_apple_id_token)
        # Make a GET request to MusicKit API
        headers = {
            'Authorization': "Bearer " + dev_token,
            'Music-User-Token': user_apple_id_token
        }
        response = requests.get("https://api.music.apple.com/v1/me/library/playlists", headers=headers)

        if response.status_code == 200:
            playlists_data = response.json().get('data', [])
            playlists = [{'name': p['attributes']['name'], 'id': p['id']} for p in playlists_data]
            print(playlists)
            return playlists
        elif response.status_code == 401:
            print("we failed pt 2")
            return None
        elif response.status_code == 403:
            print("we failed")
            return None
    except Exception as e:
        return str(e)


@app.route('/get_playlists', methods=['POST'])
def get_playlists():
    try:
        received_data = request.get_json()
        apple_id_token = received_data.get("auth_key")
        print(f"Received message: {received_data}")
        print(f"Received message: {apple_id_token}")

        dev_token = "eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlE2VEdZNUQ3TTIifQ.eyJpYXQiOjE3MTE1MzI0MjUsImV4cCI6MTcyNzA4NDQyNSwiaXNzIjoiNkJUREM3VExCViJ9.jpq9oDEOCDiv9CiZKLkU8jfD8lLxUvooeI2fcat4hHlMr9nOv69jYhuAMNzimB4fHXGUFKOO0Mxtjv_SaFCQeQ"

        # Make a GET request to MusicKit API
        headers = {
            'Authorization': "Bearer " + dev_token,
            'Music-User-Token': apple_id_token
        }
        response = requests.get("https://api.music.apple.com/v1/me/library/playlists", headers=headers)

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


@app.route('/get_access_token_spotify', methods=['POST'])
def get_access_token_spotify():
    received_data = request.get_json()
    spotify_id_token = received_data.get("auth_key")

    client_id = "6f053b82d7e849729baf10f496acae07"
    client_secret = "388cf96519ee44c2a3882c9b9315b7cf"

    encoded_credentials = base64.b64encode(client_id.encode() + b':' + client_secret.encode()).decode("utf-8")

    token_headers = {
        "Authorization": "Basic " + encoded_credentials,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    token_data = {
        "grant_type": "authorization_code",
        "code": spotify_id_token,
        "redirect_uri": "http://99.8.194.131:8000/"  # remember to change this when moving to prod
    }

    r = requests.post("https://accounts.spotify.com/api/token", data=token_data, headers=token_headers)
    print(r.json())
    token = r.json()["access_token"]
    print(token)
    return jsonify({"access_token": token})


@app.route('/get_playlists_spotify', methods=['POST'])
def get_playlists_spotify():
    try:
        # Get the current user's playlists
        received_data = request.get_json()
        spotify_id_token = received_data.get("auth_key")
        print(spotify_id_token)

        # client_id = "6f053b82d7e849729baf10f496acae07"
        # client_secret = "388cf96519ee44c2a3882c9b9315b7cf"
        #
        # encoded_credentials = base64.b64encode(client_id.encode() + b':' + client_secret.encode()).decode("utf-8")
        #
        # token_headers = {
        #     "Authorization": "Basic " + encoded_credentials,
        #     "Content-Type": "application/x-www-form-urlencoded"
        # }
        #
        # token_data = {
        #     "grant_type": "authorization_code",
        #     "code": spotify_id_token,
        #     "redirect_uri": "http://99.8.194.131:8000/"  # remember to change this when moving to prod
        # }
        #
        # r = requests.post("https://accounts.spotify.com/api/token", data=token_data, headers=token_headers)
        # print(r.json())
        # token = r.json()["access_token"]
        # print(token)
        # spToken = token

        user_headers = {
            "Authorization": "Bearer " + spotify_id_token,
            "Content-Type": "application/json"
        }

        user_params = {
            "limit": 50
        }

        user_playlists_response = requests.get("https://api.spotify.com/v1/me/playlists", params=user_params,
                                               headers=user_headers)
        print(user_playlists_response.json())

        # Format the playlists
        formatted_playlists = []
        for playlist in user_playlists_response.json()['items']:
            print("Playlist ID: " + playlist['id'] + " Name: " + playlist['name'])
            playlist_id = playlist['id']
            playlist_name = playlist['name']
            formatted_playlists.append({
                'id': playlist_id,
                'name': playlist_name
            })

        return jsonify(formatted_playlists)

    except spotipy.SpotifyException as e:
        return jsonify({'error': str(e)})


@app.route('/create_playlists_apple_music_to_spotify', methods=['POST'])
def create_playlists_apple_music_to_spotify():
    received_data = request.get_json()
    print(f"Received message: {received_data}")
    apple_id_token = received_data.get("apple_id_token")
    print(f"Received message: {apple_id_token}")
    apple_playlist_id = received_data.get("apple_playlist_id")
    print(f"Received message: {apple_playlist_id}")
    apple_playlist_name = received_data.get("apple_playlist_name")
    print(f"Received message: {apple_playlist_name}")
    spotify_id_token = received_data.get("spotify_auth_key")
    print(f"Received message: {spotify_id_token}")

    # 1. query apple music for playlist
    dev_token = "eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlE2VEdZNUQ3TTIifQ.eyJpYXQiOjE3MTE1MzI0MjUsImV4cCI6MTcyNzA4NDQyNSwiaXNzIjoiNkJUREM3VExCViJ9.jpq9oDEOCDiv9CiZKLkU8jfD8lLxUvooeI2fcat4hHlMr9nOv69jYhuAMNzimB4fHXGUFKOO0Mxtjv_SaFCQeQ"

    # Make a GET request to MusicKit API
    headers = {
        'Authorization': "Bearer " + dev_token,
        'Music-User-Token': apple_id_token
    }
    apple_response = requests.get(
        "https://api.music.apple.com/v1/me/library/playlists/{}/tracks".format(apple_playlist_id),
        headers=headers)

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

    # now in a for loop find all of the songs and add them to a new playlist in spotify
    # Get the current user's playlists

    playlist_data = {
        "name": apple_playlist_name,
        "public": True  # Set to True for a public playlist, False for private
    }

    create_playlist_url = "https://api.spotify.com/v1/me/playlists"
    headers = {
        "Authorization": f"Bearer {spotify_id_token}",
        "Content-Type": "application/json"
    }

    response = requests.post(create_playlist_url, json=playlist_data, headers=headers)
    new_playlist_id = response.json()['id']
    print(new_playlist_id)
    for song in songs:
        try:
            song_search = song['track_name']
            song_artist = song['artist_name']
            search_query = f'{song_search} {song_artist}'
            print(search_query)
            search_url = f'https://api.spotify.com/v1/search?q={search_query}&type=track&limit=3'
            headers = {
                'Authorization': f'Bearer {spotify_id_token}',
                'Content-Type': 'application/json',
            }
            response = requests.get(search_url, headers=headers)
            found_song = response.json()['tracks']['items'][0]
            print(f"Track: {found_song['name']} by {found_song['artists'][0]['name']} by {found_song['uri']}")

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
    received_data = request.get_json()
    print(f"Received message: {received_data}")
    apple_id_token = received_data.get("apple_id_token")
    print(f"Received message: {apple_id_token}")
    spotify_playlist_id = received_data.get("spotify_playlist_id")
    print(f"Received message: {spotify_playlist_id}")
    spotify_playlist_name = received_data.get("spotify_playlist_name")
    print(f"Received message: {spotify_playlist_name}")
    spotify_id_token = received_data.get("spotify_auth_key")
    print(f"Received message: {spotify_id_token}")

    # 1. query apple music for playlist
    dev_token = "eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlE2VEdZNUQ3TTIifQ.eyJpYXQiOjE3MTE1MzI0MjUsImV4cCI6MTcyNzA4NDQyNSwiaXNzIjoiNkJUREM3VExCViJ9.jpq9oDEOCDiv9CiZKLkU8jfD8lLxUvooeI2fcat4hHlMr9nOv69jYhuAMNzimB4fHXGUFKOO0Mxtjv_SaFCQeQ"

    # Make a GET request to MusicKit API
    apple_headers = {
        'Authorization': "Bearer " + dev_token,
        'Music-User-Token': apple_id_token,
        'Content-Type': 'application/json'
    }

    # query spotify for playlist
    songs = []

    spotify_playlist_url = "https://api.spotify.com/v1/me/playlists/" + spotify_playlist_id + "/tracks"
    spotify_headers = {
        "Authorization": f"Bearer {spotify_id_token}",
        "Content-Type": "application/json"
    }

    spotify_playlist_get_response = requests.get(spotify_playlist_url, headers=spotify_headers)
    spotify_playlist_get_response_json = spotify_playlist_get_response.json()

    # add all songs in playlist to list
    if spotify_playlist_get_response.status_code == 200:
        # Loop through each song in the playlist
        for item in spotify_playlist_get_response_json['items']:
            # Get the song name and artist
            song_name = item['track']['name']
            song_artist = item['track']['artists'][0]['name']
            print(f"Song: {song_name} by {song_artist}")
            songs.append((song_name, song_artist))
    else:
        print("Failed to get playlist: ", spotify_playlist_get_response_json)

    apple_songs = []
    apple_search_headers = {
        'Authorization': f'Bearer {dev_token}',
    }

    # find and add all songs
    for song in songs:
        # The song name goes here
        song_name = song[0] + " " + song[1]
        response = requests.get(f'https://api.music.apple.com/v1/catalog/us/songs?filter[term]={song_name}',
                                headers=apple_search_headers)
        response_json = response.json()
        # Check if the request was successful
        if response.status_code == 200:
            # Check if 'results' is not empty and contains an 'id' field
            if response_json.get('results') and 'id' in response_json['results'][0]:
                # Loop through each song in the response
                apple_songs.append(response_json['results'][0]['id'])
            else:
                print("Failed to get song ID: ", response_json)
        else:
            print("Failed to get songs: ", response_json)

    # The playlist details go here
    playlist_details = {
        "attributes": {
            "name": spotify_playlist_name,
            "description": "Generated Playlist from Spotify",
            "tracks": apple_songs
        }
    }

    apple_response = requests.post('https://api.music.apple.com/v1/me/library/playlists', headers=apple_headers,
                                   data=json.dumps(playlist_details))
    print(apple_response.status_code)
    return {}


if __name__ == '__main__':
    app.run(debug=True)
