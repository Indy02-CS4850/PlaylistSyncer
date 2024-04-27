import 'dart:developer';
import 'package:flutter/material.dart';
import 'dart:js' as js;

// don't ask why flutters decoder for json doesnt work.
List<Map<String, String>> customDecode(String jsonString) { // This is what gets the playlist names/ids
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

List<Map<String, String>> readApplePlaylistJSON() { // This gets called in js
  var state = js.JsObject.fromBrowserObject(js.context['applePlaylistState']);
  String jsonString = state['Playlists'];

  List<Map<String, String>> applePlaylists = customDecode(jsonString);
  return applePlaylists;
} // Returns a list of playlist IDs and Names

List<Map<String, String>> readSpotifyPlaylistJSON() { // This gets called in js
  var state = js.JsObject.fromBrowserObject(js.context['spotifyPlaylistState']);
  String jsonString = state['Playlists'];
  log(jsonString);

  List<Map<String, String>> spotifyPlaylists = customDecode(jsonString);
  return spotifyPlaylists;
} // Returns a list of playlist IDs and Names

// Future<void> authenticateSpotify() async {
//   final result = await FlutterWebAuth.authenticate(url: "https://accounts.spotify.com/authorize?client_id=6f053b82d7e849729baf10f496acae07&redirect_uri=http://99.8.194.131:8000/&scope=user-library-read playlist-modify-private playlist-modify-public playlist-read-private playlist-read-collaborative&response_type=code", callbackUrlScheme: "my-custom-app");
// }

void dropdownPlaylists(List<String> buttonOrder) {
    String platform = buttonOrder.first;
    if(platform == 'Spotify'){
      decodedPlaylists = readSpotifyPlaylistJSON();
      // Done because I didn't want to run into issues whilst testing
      // decodedPlaylists = readApplePlaylistJSON();
    }
    else if(platform == 'Apple Music'){
      decodedPlaylists = readApplePlaylistJSON();
    }
} // Assigns values to the transfer dropdown dependent on the first button selected

List<Map<String, String>> decodedPlaylists = [];
// Not ideal to have a global here, but for now it will have to do.


void main() {
  // runApp(const MyApp());
  js.context['readApplePlaylistJSON'] = js.allowInterop(readApplePlaylistJSON);
  js.context['readSpotifyPlaylistJSON'] = js.allowInterop(readSpotifyPlaylistJSON);
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

    @override
    Widget build(BuildContext context) {
        return MaterialApp(
            debugShowCheckedModeBanner: false,
            title: "Test App",
            theme: ThemeData.dark(),
            home: DefaultTabController(
              length: 3,
              child: Scaffold(
                appBar: AppBar(
                  title: const Text("Playlist Syncher"),
                  flexibleSpace: Container(
                    decoration: const BoxDecoration(
                      gradient: LinearGradient(
                        begin: Alignment.topLeft,
                        end: Alignment.bottomRight,
                        colors: <Color>[
                          Color.fromARGB(255, 37, 216, 101),
                          Color.fromARGB(255, 242, 166, 12),
                          Color.fromARGB(255, 251, 35, 60)
                        ]
                      )
                    ),
                  ),
                  centerTitle: true,
                  bottom: const TabBar(
                    tabs: [
                      Tab(text: 'Authentication'),
                      Tab(text: 'Transfer'),
                      Tab(text: 'Settings'),
                    ],
                  ),
                ),
                body: TabBarView(
                  children: [
                    Container(
                      padding: const EdgeInsets.all(20),
                      child: Center(
                        child: Column(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            ElevatedButton(
                              onPressed: () async {
                                // js.context.callMethod("spotifyAuthUser");
                                // js.context.callMethod('spotifyAuthUser');
                                final currentUrl = Uri.base;
                                if(currentUrl.queryParameters.containsKey('code')){
                                  final code = currentUrl.queryParameters['code'];
                                  print('Recieved code: $code');
                                  js.context.callMethod('spotifyAccessTokenGet', [code]);
                                }else{
                                  js.context.callMethod('spotifyAuthUser');
                                }
                              },
                              child: const Text("Authenticate spotify"),
                            ),
                            const SizedBox(height: 16), // Add some spacing between buttons
                            ElevatedButton(
                              onPressed: () {
                                // final currentUrl = Uri.base;
                                // if(currentUrl.queryParameters.containsKey('code')){
                                //   final code = currentUrl.queryParameters['code'];
                                //   print('Recieved code: $code');
                                //   js.context.callMethod('spotifyPlaylistGet', [code]);
                                // }
                                var spotifyState = js.JsObject.fromBrowserObject(js.context['spotifyPlaylistState']);
                                String spotifyIDString = spotifyState['access_token'];
                                js.context.callMethod('spotifyPlaylistGet', [spotifyIDString]);
                              },
                              child: const Text("Retrieve Spotify playlist data"),
                            ),
                            const SizedBox(height: 16), // Add some spacing between buttons
                            ElevatedButton(
                              onPressed: () {
                                js.context.callMethod("appleAuthUser");
                              },
                              child: const Text("Authenticate Apple Music"),
                            ),
                            const SizedBox(height: 16), // Add some spacing between buttons
                            ElevatedButton(
                              onPressed: () {
                                js.context.callMethod('applePlaylistGet');
                              },
                              child: const Text("Retrieve Apple Music playlist data"),
                            ),
                            // ElevatedButton(
                            //   onPressed: () {
                            //     var appleState = js.JsObject.fromBrowserObject(js.context['applePlaylistState']);
                            //     String appleIDString = appleState['Apple_ID_Token'];
                            //     var spotifyState = js.JsObject.fromBrowserObject(js.context['spotifyPlaylistState']);
                            //     String spotifyIDString = spotifyState['access_token'];
                            //     js.context.callMethod('createPlaylistfromAppleMusicToSpotify', [appleIDString,"p.mDxCgx0Bz3","Firewatch",spotifyIDString]); // this is an example playlist
                            //   },
                            //   child: const Text("test Playlist transfer"),
                            // ),
                          ],
                        ),
                      ),
                    ),
                    const Center(child: TransferProcess()), // This is what is on each page
                    const Center(child: Text('Plans to change theme here')), // This is what is on each page
                ],
              ),
            ),
      ),
    );
  }
}

class TransferProcess extends StatefulWidget {
  const TransferProcess({super.key});

  @override
  _TransferProcessState createState() => _TransferProcessState();
}

class _TransferProcessState extends State<TransferProcess> with SingleTickerProviderStateMixin {
  List<String> buttonOrder = [];
  String dropdownValue = 'Option 1';
  late AnimationController _controller;
  late Animation<double> _animation;

  String getSelectedPlaylist(){
    return dropdownValue;
  }

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      duration: const Duration(seconds: 2),
      vsync: this,
    )..addListener(() {
      setState(() {});
    });
    _animation = CurvedAnimation(
      parent: _controller, 
      curve: Curves.easeIn,
    );
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      mainAxisAlignment: MainAxisAlignment.center,
      children: <Widget>[
        Text(
          buttonOrder.isEmpty 
            ? 'What Platform would you like to transfer from?' 
              :buttonOrder.length == 1
                ? 'You are currently transferring from: ${buttonOrder.join(', ')}, where would you like to transfer to?'
                  : 'Transferring from ${buttonOrder.join(' to ')}',
        ),
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceAround,
          children: <Widget>[
          Align(
          alignment: Alignment.centerLeft,
          child: ElevatedButton(
            onPressed: (){
              setState(() {
                if(buttonOrder.length < 2){
                  buttonOrder.add('Spotify');
                }
                if(buttonOrder.length == 2){
                  dropdownPlaylists(buttonOrder);
                  dropdownValue = decodedPlaylists[0]['name']!;
                  _controller.forward();
                }
              });
            },
            child: const Text('Spotify'),
          ),
        ),
        Align(
          alignment: Alignment.centerRight,
          child: ElevatedButton(
            onPressed: (){
              setState(() {
                if(buttonOrder.length < 2){
                  buttonOrder.add('Apple Music');
                }
                if(buttonOrder.length == 2){
                  dropdownPlaylists(buttonOrder);
                  dropdownValue = decodedPlaylists[0]['name']!;
                  _controller.forward();
                }
              });
            }, 
            child: const Text('Apple Music'),
          ),
        ),
          ],
        ),
        if(buttonOrder.length == 2) // From this spot downwards is where I will need to add flask to denote user selecting an option ( I think adding another button that sends off the currently selected dropdown )
          FadeTransition(
            opacity: _animation,
            child: Column(
              children: <Widget>[
                const Padding(
                  padding: EdgeInsets.all(8.0),
                  child: Text('Select a Playlist'),
                ),
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 10.0),
              decoration: BoxDecoration(
                color: Colors.white,
                borderRadius: BorderRadius.circular(30.0),
                border: Border.all(
                  color: Colors.blue,
                  width: 2.0,
                ),
              ),
              child: DropdownButtonHideUnderline(
                child: DropdownButton<String>(
            value: dropdownValue,
            onChanged: (String? newValue) {
              setState(() {
                dropdownValue = newValue ?? ''; // Basically means it can be a string or null
              });
            },
            items: decodedPlaylists.map<DropdownMenuItem<String>>((Map<String, String> playlist) { 
              String name = playlist['name']!;
              return DropdownMenuItem<String>(
                value: name,
                child: Text(name),
              );
            }).toList(),
          ),
         ),
        ),
        Align(
          alignment: Alignment.bottomRight,
          child: ElevatedButton(
            onPressed: () {
              String playlistName = getSelectedPlaylist();
              print(playlistName); // Testing purposes
              String platformFrom = buttonOrder.first;
              print(platformFrom); // Testing purposes

               var appleState = js.JsObject.fromBrowserObject(js.context['applePlaylistState']);
                String appleIDString = appleState['Apple_ID_Token'];
                var spotifyState = js.JsObject.fromBrowserObject(js.context['spotifyPlaylistState']);
                String spotifyIDString = spotifyState['access_token'];
                int index = decodedPlaylists.indexWhere((map) => map['name'] == playlistName);
                print(index);

              if(platformFrom == "Apple Music"){
                js.context.callMethod('createPlaylistfromAppleMusicToSpotify', [appleIDString,decodedPlaylists[index]['id'],playlistName,spotifyIDString]);
              } else if (platformFrom == "Spotify"){
                js.context.callMethod('createPlaylistfromSpotifyToAppleMusic', [appleIDString,decodedPlaylists[index]['id'],playlistName,spotifyIDString]);
              }
              // Start a method here that takes these both and sends them to flask for the
              // get playlist data, sync, and create playlist. For now just assume that 
              // whatever platform was pressed first is transferring to the other option
            },
            child: const Text("Start Transfer"),
          ),
        ),
              ],
            ),
        ),
      ],
    );
  }
}