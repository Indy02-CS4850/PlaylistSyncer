window.createPlaylistfromAppleMusicToSpotify = function(apple_id_token,apple_playlist_id,apple_playlist_name,spotify_auth_key) {
    fetch("http://127.0.0.1:5000/create_playlists_apple_music_to_spotify", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        "apple_id_token": apple_id_token,
        "apple_playlist_id": apple_playlist_id,
        "apple_playlist_name": apple_playlist_name,
        "spotify_auth_key": spotify_auth_key
    })
    })
      .then(response => response.json())
    //   .then(data => {
    //     pain = JSON.stringify(data)
    //     window.applePlaylistState.Playlists = pain;
    //     console.log("Received data from Flask: " + pain);
    //     readApplePlaylistJSON();
    //   })
    //   .catch(error => {
    //     console.error("Error sending auth key:" + toString(error));
    //   });
}