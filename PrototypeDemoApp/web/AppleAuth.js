// web/AppleAuth.js

userToken = ""; //gets filledin by user when they login

// function to authenticate Apple Music Users
function appleAuthUser() {
    devToken = ""

    fetch("http://99.8.194.131:5000/get_apple_data", {
      method: "GET",
      headers: {
        "Content-Type": "application/json"
      }
    }).then(response => response.json()).then(data => {
      devToken = data.apple_dev_token;
      MusicKit.configure({
        developerToken: devToken,
        app: {
            name: "OurApp",
            build: "1.0"
        }
    });

    let music = MusicKit.getInstance();

    music.authorize().then((token) => {
        userToken = token;
        window.applePlaylistState.Apple_ID_Token = userToken;
    });
    })
}

// temp datastore for playlists
window.applePlaylistState = {};

//get playlist data then if valid update window.state and call the dart function to read the data
window.applePlaylistGet = function() {
    fetch("http://99.8.194.131:5000/get_playlists_apple", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ "auth_key": userToken })
    })
      .then(response => response.json())
      .then(data => {
        playlist = JSON.stringify(data)
        window.applePlaylistState.Playlists = playlist;
        readApplePlaylistJSON();
      })
      .catch(error => {
        console.error("Error sending auth key:" + toString(error));
      });
}