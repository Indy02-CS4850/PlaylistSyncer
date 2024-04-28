// // web/SpotifyAuth.js

// temp datastore for playlists
window.spotifyPlaylistState = {};

const redirect_uri = ''; // Your callback URL for spotify
var url = "";
var port = "";

// Redirect the user to Spotify's authorization page
window.spotifyAuthUser = function() {
    client_id = ""
    //fetch client if from flask server and use it to access spoitfy services
    fetch(`${url}:${port}/get_spotify_data`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json"
      }
    }).then(response => response.json()).then(data => {
      client_id = data.spotify_client_id;
      const authUrl = `https://accounts.spotify.com/authorize?client_id=${client_id}&response_type=code&redirect_uri=${encodeURIComponent(redirect_uri)}&scope=playlist-modify-private user-library-read playlist-modify-public playlist-read-private playlist-read-collaborative`;
      window.location.href = authUrl;
    })
}

// generate a user access token on the flask server based on user token
window.spotifyAccessTokenGet = function(userToken) {
  fetch(`${url}:${port}/get_access_token_spotify`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ "auth_key": userToken })
    })
      .then(response => response.json())
      .then(data => {
        window.spotifyPlaylistState.access_token = data.access_token;
      })
      .catch(error => {
        console.error("Error sending auth key:" + toString(error));
      });
}

//get playlist data then if valid update window.state and call the dart function to read the data
window.spotifyPlaylistGet = function(access_token) {
  fetch(`${url}:${port}/get_playlists_spotify`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ "auth_key": access_token })
    })
      .then(response => response.json())
      .then(data => {
        playlist = JSON.stringify(data)
        window.spotifyPlaylistState.Playlists = playlist;
        readSpotifyPlaylistJSON();
      })
      .catch(error => {
        console.error("Error sending auth key:" + toString(error));
      });
}