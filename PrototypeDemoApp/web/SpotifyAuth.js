// // web/script.js
// const clientId = '6f053b82d7e849729baf10f496acae07';
// const clientSecret = '388cf96519ee44c2a3882c9b9315b7cf';
// const redirectUri = 'http://localhost:53519/'; //change this on push to prod
// const scopes = ['user-read-private', 'user-read-email'];

// temp datastore for playlists
window.spotifyPlaylistState = {};

//get playlist data then if valid update window.state and call the dart function to read the data
// window.spotifyAuthUser = function(spotifyUserToken) {
//     console.log(spotifyUserToken);
//     userToken = spotifyUserToken;
// }

const client_id = '6f053b82d7e849729baf10f496acae07';
const client_secret = '388cf96519ee44c2a3882c9b9315b7cf';
const redirect_uri = 'http://localhost:8000/'; // Your callback URL
// var userToken = "";

// Step 1: Redirect the user to Spotify's authorization page
window.spotifyAuthUser = function() {
    const authUrl = `https://accounts.spotify.com/authorize?client_id=${client_id}&response_type=code&redirect_uri=${encodeURIComponent(redirect_uri)}&scope=user-library-read playlist-modify-private playlist-modify-public playlist-read-private playlist-read-collaborative`;
    window.location.href = authUrl;
}

// window.spotifyGetCodeFromURL = function() {
//   const code = new URLSearchParams(window.location.search).get('code');
//   if (code) {
//     spotifyPlaylistGet(code)
//       // // Step 3: Exchange the authorization code for an access token
//       // fetch('https://accounts.spotify.com/api/token', {
//       //     method: 'POST',
//       //     body: `grant_type=authorization_code&code=${code}&redirect_uri=${encodeURIComponent(redirect_uri)}`,
//       //     headers: {
//       //         'Content-Type': 'application/x-www-form-urlencoded',
//       //         'Authorization': `Basic ${btoa(`${client_id}:${client_secret}`)}` // Base64-encoded client credentials
//       //     }
//       // })
//       // .then(response => response.json())
//       // .then(data => {
//       //     const accessToken = data.access_token;
//       //     console.log('User access token:', accessToken);
//       //     userToken = accessToken;
//       //     // You can use the access token for Spotify API requests
//       // })
//       // .catch(error => {
//       //     console.error('Error fetching token:', error);
//       // });
//   } else {
//       console.error('Authorization code not found.');
//   }
// }

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