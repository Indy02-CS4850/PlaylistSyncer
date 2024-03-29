import 'dart:convert' as convert;
import 'dart:js_interop';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:js' as js;

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

void readApplePlaylistJSON() {
  var state = js.JsObject.fromBrowserObject(js.context['applePlaylistState']);
  String jsonString = state['Playlists'];

  List<Map<String, String>> decodedPlaylists = customDecode(jsonString);
}

void main() {
  // runApp(const MyApp());
  js.context['readApplePlaylistJSON'] = js.allowInterop(readApplePlaylistJSON);
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
                  onPressed: () {
                    js.context.callMethod("appleAuthUser");
                  },
                  child: const Text("Authenticate Apple Music"),
                ),
                SizedBox(height: 16), // Add some spacing between buttons
                ElevatedButton(
                  onPressed: () {
                    js.context.callMethod('applePlaylistGet');
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