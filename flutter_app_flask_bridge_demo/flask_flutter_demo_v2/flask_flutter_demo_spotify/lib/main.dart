import 'dart:convert' as convert;
import 'dart:developer';
import 'dart:html';
import 'dart:js_interop';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:js' as js;
import 'package:spotify_sdk/spotify_sdk.dart';
import 'package:flutter_web_auth/flutter_web_auth.dart';

// don't ask why flutters decoder for json doesnt work.
List<Map<String, String>> customDecode(String jsonString) {
  // Remove the enclosing square brackets to get the inner JSON array
  String trimmedJsonString = jsonString.substring(1, jsonString.length - 1);

  // Split the string by '},{"' to separate individual playlist entries
  List<String> playlistEntries = trimmedJsonString.split('},{');

  // Initialize an empty list to store the parsed playlists
  List<Map<String, String>> playlists = [];

  for (var entry in playlistEntries) {
    // Add back the curly braces to each entry
    String playlistJson = '{$entry}';

    // Extract the id and name using text parsing
    String id = playlistJson.split('"id":"')[1].split('","name"')[0];
    String name = playlistJson.split('"name":"')[1].split('"}')[0];

    // Create a map for the playlist
    Map<String, String> playlist = {'id': id, 'name': name};
    playlists.add(playlist);
  }

  // Print playlist names and IDs
  for (var playlist in playlists) {
    print('Playlist ID: ${playlist['id']}, Name: ${playlist['name']}');
  }

  return playlists;
}

void readSpotifyPlaylistJSON() {
  var state = js.JsObject.fromBrowserObject(js.context['spotifyPlaylistState']);
  String jsonString = state['Playlists'];
  log(jsonString);

  List<Map<String, String>> decodedPlaylists = customDecode(jsonString);
}

Future<void> authenticateSpotify() async {
  final result = await FlutterWebAuth.authenticate(url: "https://accounts.spotify.com/authorize?client_id=6f053b82d7e849729baf10f496acae07&redirect_uri=http://localhost:8000/&scope=user-library-read playlist-modify-private playlist-modify-public playlist-read-private playlist-read-collaborative&response_type=code", callbackUrlScheme: "my-custom-app");
}

void main() {
  // runApp(const MyApp());
  js.context['readSpotifyPlaylistJSON'] = js.allowInterop(readSpotifyPlaylistJSON);
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
    @override
    Widget build(BuildContext context) {
        return MaterialApp(
            title: "Test App",
            home: Scaffold(
                appBar: AppBar(
                    title: Text("Call JS Function"),
                    backgroundColor: Colors.redAccent,
                ),
                body: Container(
          padding: EdgeInsets.all(20),
          child: Center(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                ElevatedButton(
                  onPressed: () async {
                    // js.context.callMethod("spotifyAuthUser");
                    final currentUrl = Uri.base;

                    // Check if the 'code' parameter exists
                    if (currentUrl.queryParameters.containsKey('code')) {
                      final code = currentUrl.queryParameters['code'];
                      print('Received code: $code'); // Print to debug console
                      js.context.callMethod('spotifyAuthUser', [code]);
                    } else {
                      authenticateSpotify();
                    }
                  },
                  child: const Text("Authenticate spotify"),
                ),
                SizedBox(height: 16), // Add some spacing between buttons
                ElevatedButton(
                  onPressed: () {
                    js.context.callMethod('spotifyPlaylistGet');
                  },
                  child: const Text("Retrieve playlist data"),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}