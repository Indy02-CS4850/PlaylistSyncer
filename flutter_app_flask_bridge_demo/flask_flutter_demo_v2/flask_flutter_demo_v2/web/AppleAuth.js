// web/script.js
devToken = "eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlE2VEdZNUQ3TTIifQ.eyJpYXQiOjE3MTE1MzI0MjUsImV4cCI6MTcyNzA4NDQyNSwiaXNzIjoiNkJUREM3VExCViJ9.jpq9oDEOCDiv9CiZKLkU8jfD8lLxUvooeI2fcat4hHlMr9nOv69jYhuAMNzimB4fHXGUFKOO0Mxtjv_SaFCQeQ";
userToken = "";

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
        console.log("token is: " + token);
        userToken = token;
    });
}

function applePlaylistGet(){
    // console.log("User token: " + userToken)
    // apple_id_user_token = userToken

    // fetchRequestTest()
    fetch("http://127.0.0.1:5000/get_playlists", {
        method: "POST",
        headers: {
            "Content-Type": "application/json" // Set the content type
        },
        body: JSON.stringify({ "auth_key": userToken })
    }).then(response => response.json())
        .then(data => {
            console.log("Received from Flask:", data.response);
        })
        .catch(error => {
            console.error("Error sending auth key:", error);
        });
}

// function fetchRequestTest(){
//     const apiUrl = "https://api.music.apple.com/v1/me/library/songs";

//     // Make an HTTP request to fetch the user's playlists
//     fetch(apiUrl, {
//     method: 'GET',
//     headers: {
//         "Authorization": "eyJhbGciOiJFUzI1NiIsImlzcyI6IlE2VEdZNUQ3TTIiLCJraWQiOiI2QlREQzdUTEJWIiwidHlwIjoiSldUIn0.eyJpc3MiOiI2OWE2ZGU5NS0wMjNmLTQ3ZTMtZTA1My0xMmxqbGVpbzNrYWp2emJ2IiwiaWF0IjoxNzExNzAxOTU2LCJleHAiOjE3MTE3MDMwOTYsImF1ZCI6ImFwcHN0b3JlY29ubmVjdC12MSJ9.y82ONrf1zz_NmJ_47eaGGNgyqNGpApWBGhumXkeXTGDvJlR-eVmJvjVFPWRRVYvQlLmbXzQD6ikPyClIO-2VnA",
//         'Music-User-Token': "Ap4/IYeccFfrD5P98RmmgKpG/PWurHNkjJlNHXFQ+gYZ4RMqnhR1uNi373JrBhI2JfTmSS8OkWvcTicJC2Cl3wlTikfAUc17al1BUM/P4bfOeXD9Lx4z6mV2zvsxvpTSrinDZhJj0X/PgJaNRvauixP3wQyd/Wf8iMpQMYUxDK0+KFYSh1Ya2VGkgptCi1/Rrq3+TthphLvaiSEptEx6rKzozCf3sFLIQzqGbUizv62QWQ3HXA==", 
//     },
//     })
//     .then((response) => response.json())
//     .then((data) => {
//         // Process the data (e.g., extract playlist names, track IDs, etc.)
//         console.log('User playlists:', data);
//     })
//     .catch((error) => {
//         console.error('Error fetching playlists:', error);
//     });
// }