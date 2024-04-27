PlaylistSyncer setup guide:
--- Flask Setup---
1.	Open app.py from the Final_Flask_Server_SRC folder
2.	Define your Spotify redirect URL on line 14; this should reflect your Flutter web server IP and should be the same as the redirect URL you have created in Spotify’s developer portal
3.	Add three files: Apple_dev_token.txt, spotify_client.id.txt, and Spotify_client_secret.txt; these files should be in the same directory as an app.py
a.	Apple_dev_token.txt contains your Apple app developer JWT string 
b.	spotify_client.id.txt contains your Spotify app client id
c.	spotify_client_secret.txt contains your Spotify app secret key
4.	run the app using sudo flask run –host=[YOUR_SERVER_IP_HERE]
--- Flutter Setup---
1.	Open the Final_Flutter_WebApp_SRC folder in VS Code
2.	In PlaylistTransfer.js, on lines 1,2, set the url and port vars to the url and port of the flask server
3.	In appleAuth.js, on line 5,6, set the url and port vars to the url and port of the flask server
4.	In SpotifyAuth.js, on lines 7,8, set the url and port vars to the url and port of the flask server
5.	Run “flutter build web” in the Final_Flutter_WebApp_SRC directory, make a note of the web folder in the build folder; this is the code you will use to host the website
--- Completing your first Playlist Transfer! ---
1.	Navigate to the URL/Domain for your Flutter app in your web browser while the Flask server and Flutter app are running
2.	On the authenticate page, press the “Authenticate Spotify” button
3.	After signing in through Spotify and being redirected back to the website, press “Authenticate Spotify” again to grab the authentication code from the redirect URI
4.	Press “Retrieve Spotify Playlist Data” to grab all your playlists from Spotify
5.	Press the “Authenticate Apple Music” button and then sign in through the Apple Music pop-up window
6.	Press “Retrieve Apple Music Playlist Data” to grab all your playlists from Apple Music
7.	Press on the “Transfer” page
8.	Select “Spotify” or “Apple Music” from the two available buttons
9.	Select “Spotify” or “Apple Music” from the two available buttons based on which button you pressed previously; for example, if you selected Spotify, you should now choose Apple Music
10.	Select a playlist from the dropdown list, then press “Start Transfer” to begin 
