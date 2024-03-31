// temp datastore for playlists
window.spotifyPlaylistState = {};

const client_id = '6f053b82d7e849729baf10f496acae07';
const client_secret = '388cf96519ee44c2a3882c9b9315b7cf';
const redirect_uri = 'http://localhost:8000/'; // Your callback URL

window.spotifyAuthUser = function() {
    const authUrl = `https://accounts.spotify.com/authorize?client_id=${client_id}&response_type=code&redirect_uri=${encodeURIComponent(redirect_uri)}&scope=user-library-read playlist-modify-private playlist-modify-public playlist-read-private playlist-read-collaborative`;
    window.location.href = authUrl;
}

window.spotifyPlaylistGet = function(userToken) {
  console.log(userToken);
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