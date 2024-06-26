var url = "http://99.8.194.131";
var port = "5000";

window.createPlaylistfromAppleMusicToSpotify = function(apple_id_token,apple_playlist_id,apple_playlist_name,spotify_auth_key) {
    fetch(`${url}:${port}/create_playlists_apple_music_to_spotify`, {
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
}

window.createPlaylistfromSpotifyToAppleMusic = function(apple_id_token,spotify_playlist_id,spotify_playlist_name,spotify_auth_key) {
  fetch(`${url}:${port}/create_playlists_spotify_to_apple_music`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      "apple_id_token": apple_id_token,
      "spotify_playlist_id": spotify_playlist_id,
      "spotify_playlist_name": spotify_playlist_name,
      "spotify_auth_key": spotify_auth_key
  })
  })
    .then(response => response.json())
}