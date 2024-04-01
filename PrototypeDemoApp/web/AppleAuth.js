// web/script.js
devToken = "eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlE2VEdZNUQ3TTIifQ.eyJpYXQiOjE3MTE1MzI0MjUsImV4cCI6MTcyNzA4NDQyNSwiaXNzIjoiNkJUREM3VExCViJ9.jpq9oDEOCDiv9CiZKLkU8jfD8lLxUvooeI2fcat4hHlMr9nOv69jYhuAMNzimB4fHXGUFKOO0Mxtjv_SaFCQeQ";
userToken = ""; //gets filledin by user when they login

// function to authenticate Apple Music Users
function appleAuthUser() {
    MusicKit.configure({
        developerToken: devToken,
        app: {
            name: "OurApp",
            build: "1.0"
        }
    });

    let music = MusicKit.getInstance();

    music.authorize().then((token) => {
        console.log("authorized");
        // console.log("token is: " + token);
        userToken = token;
        window.applePlaylistState.Apple_ID_Token = userToken;
        console.log("token is: " + userToken)
    });
}

// temp datastore for playlists
window.applePlaylistState = {};

//get playlist data then if valid update window.state and call the dart function to read the data
window.applePlaylistGet = function() {
    fetch("http://127.0.0.1:5000/get_playlists", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ "auth_key": userToken })
    })
      .then(response => response.json())
      .then(data => {
        pain = JSON.stringify(data)
        window.applePlaylistState.Playlists = pain;
        console.log("Received data from Flask: " + pain);
        readApplePlaylistJSON();
      })
      .catch(error => {
        console.error("Error sending auth key:" + toString(error));
      });
}