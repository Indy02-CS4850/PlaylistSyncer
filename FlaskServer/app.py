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

        # print("Suicide Note: " + apple_id_token)
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


@app.route('/get_playlists_spotify', methods=['POST'])
def get_playlists_spotify():
    try:
        # Get the current user's playlists
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
            "redirect_uri": "http://localhost:8000/" # remember to change this when moving to prod
        }

        r = requests.post("https://accounts.spotify.com/api/token", data=token_data, headers=token_headers)
        print(r.json())
        token = r.json()["access_token"]
        print(token)

        user_headers = {
            "Authorization": "Bearer " + token,
            "Content-Type": "application/json"
        }

        user_params = {
            "limit": 50
        }

        user_playlists_response = requests.get("https://api.spotify.com/v1/me/playlists", params=user_params,headers=user_headers)
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


if __name__ == '__main__':
    app.run(debug=True)
