// web/script.js
const clientId = '6f053b82d7e849729baf10f496acae07';
const clientSecret = '388cf96519ee44c2a3882c9b9315b7cf';
const redirectUri = 'http://localhost:53519/'; //change this on push to prod
const scopes = ['user-read-private', 'user-read-email'];
var userToken = "";

// temp datastore for playlists
window.spotifyPlaylistState = {};

//get playlist data then if valid update window.state and call the dart function to read the data
window.spotifyAuthUser = function(spotifyUserToken) {
    console.log(spotifyUserToken);
    userToken = spotifyUserToken;
}

window.spotifyPlaylistGet = function() {
  fetch("http://127.0.0.1:5000/get_playlists_spotify", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ "auth_key": userToken })
    })
      .then(response => response.json())
      .then(data => {
        pain = JSON.stringify(data)
        window.spotifyPlaylistState.Playlists = pain;
        console.log("Received data from Flask: " + pain);
        readSpotifyPlaylistJSON();
      })
      .catch(error => {
        console.error("Error sending auth key:" + toString(error));
      });
}