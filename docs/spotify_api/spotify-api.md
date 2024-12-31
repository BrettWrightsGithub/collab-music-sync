## Access Token
The access token is a string which contains the credentials and permissions that can be used to access a given resource (e.g artists, albums or tracks) or user's data (e.g your profile or your playlists).
To use the access token you must include the following header in your API calls:
Header Parameter	Value
Authorization	Valid access token following the format: Bearer <Access Token>
Note that the access token is valid for 1 hour (3600 seconds). After that time, the token expires and you need to request a new one.
Examples
The following example uses cURL to retrieve information about a track using the Get a track endpoint:
curl --request GET \
    'https://api.spotify.com/v1/tracks/2TpxZ7JUBn3uw46aR7qd6V' \
     --header "Authorization: Bearer NgCXRK...MzYjw"

The following code implements the getProfile() function which performs the API call to the Get Current User's Profile endpoint to retrieve the user profile related information:
async function getProfile(accessToken) {
  let accessToken = localStorage.getItem('access_token');

  const response = await fetch('https://api.spotify.com/v1/me', {
    headers: {
      Authorization: 'Bearer ' + accessToken
    }
  });

  const data = await response.json();
}

Client Credentials Flow
The Client Credentials flow is used in server-to-server authentication. Since this flow does not include authorization, only endpoints that do not access user information can be accessed.
The following diagram shows how the Client Credentials Flow works:
Client Credentials Flow
Pre-requisites
This guide assumes that:
You have read the authorization guide.
You have created an app following the app guide.
Source Code
You can find an example app implementing Client Credentials flow on GitHub in the web-api-examples repository.
Request authorization
The first step is to send a POST request to the /api/token endpoint of the Spotify OAuth 2.0 Service with the following parameters encoded in application/x-www-form-urlencoded:
Body Parameters	Relevance	Value
grant_type	Required	Set it to client_credentials.
The headers of the request must contain the following parameters:
Header Parameter	Relevance	Value
Authorization	Required	Base 64 encoded string that contains the client ID and client secret key. The field must have the format: Authorization: Basic <base64 encoded client_id:client_secret>
Content-Type	Required	Set to application/x-www-form-urlencoded.
The following JavaScript creates and sends an authorization request:
var client_id = 'CLIENT_ID';
var client_secret = 'CLIENT_SECRET';

var authOptions = {
  url: 'https://accounts.spotify.com/api/token',
  headers: {
    'Authorization': 'Basic ' + (new Buffer.from(client_id + ':' + client_secret).toString('base64'))
  },
  form: {
    grant_type: 'client_credentials'
  },
  json: true
};

request.post(authOptions, function(error, response, body) {
  if (!error && response.statusCode === 200) {
    var token = body.access_token;
  }
});

Response
If everything goes well, you'll receive a response with a 200 OK status and the following JSON data in the response body:
key	Type	Description
access_token	string	An access token that can be provided in subsequent calls, for example to Spotify Web API services.
token_type	string	How the access token may be used: always "Bearer".
expires_in	int	The time period (in seconds) for which the access token is valid.
For example:
{
   "access_token": "NgCXRKc...MzYjw",
   "token_type": "bearer",
   "expires_in": 3600
}

What's next?
Learn how to use an access token to fetch data from the Spotify Web API by reading the access token guide.

## API calls
The Spotify Web API is a restful API with different endpoints which return JSON metadata about music artists, albums, and tracks, directly from the Spotify Data Catalogue.
Base URL
The base address of Web API is https://api.spotify.com.
Authorization
All requests to Spotify Web API require authorization. Make sure you have read the authorization guide to understand the basics.
To access private data through the Web API, such as user profiles and playlists, an application must get the user’s permission to access the data.
Requests
Data resources are accessed via standard HTTP requests in UTF-8 format to an API endpoint. The Web API uses the following HTTP verbs:
Method	Action
GET	Retrieves resources
POST	Creates resources
PUT	Changes and/or replaces resources or collections
DELETE	Deletes resources
Responses
Web API normally returns JSON in the response body. Some endpoints (e.g Change Playlist Details) don't return JSON but the HTTP status code
Response Status Codes
Web API uses the following response status codes, as defined in the RFC 2616 and RFC 6585:
Status Code	Description
200	OK - The request has succeeded. The client can read the result of the request in the body and the headers of the response.
201	Created - The request has been fulfilled and resulted in a new resource being created.
202	Accepted - The request has been accepted for processing, but the processing has not been completed.
204	No Content - The request has succeeded but returns no message body.
304	Not Modified. See Conditional requests.
400	Bad Request - The request could not be understood by the server due to malformed syntax. The message body will contain more information; see Response Schema.
401	Unauthorized - The request requires user authentication or, if the request included authorization credentials, authorization has been refused for those credentials.
403	Forbidden - The server understood the request, but is refusing to fulfill it.
404	Not Found - The requested resource could not be found. This error can be due to a temporary or permanent condition.
429	Too Many Requests - Rate limiting has been applied.
500	Internal Server Error. You should never receive this error because our clever coders catch them all ... but if you are unlucky enough to get one, please report it to us through a comment at the bottom of this page.
502	Bad Gateway - The server was acting as a gateway or proxy and received an invalid response from the upstream server.
503	Service Unavailable - The server is currently unable to handle the request due to a temporary condition which will be alleviated after some delay. You can choose to resend the request again.
Response Error
Web API uses two different formats to describe an error:
Authentication Error Object
Regular Error Object
Authentication Error Object
Whenever the application makes requests related to authentication or authorization to Web API, such as retrieving an access token or refreshing an access token, the error response follows RFC 6749 on the OAuth 2.0 Authorization Framework.
Key	Value Type	Value Description
error	string	A high level description of the error as specified in RFC 6749 Section 5.2.
error_description	string	A more detailed description of the error as specified in RFC 6749 Section 4.1.2.1.
Here is an example of a failing request to refresh an access token.
$ curl -H "Authorization: Basic Yjc...cK" -d grant_type=refresh_token -d refresh_token=AQD...f0 "https://accounts.spotify.com/api/token"

{
    "error": "invalid_client",
    "error_description": "Invalid client secret"
}

Regular Error Object
Apart from the response code, unsuccessful responses return a JSON object containing the following information:
Key	Value Type	Value Description
status	integer	The HTTP status code that is also returned in the response header. For further information, see Response Status Codes.
message	string	A short description of the cause of the error.
Here, for example is the error that occurs when trying to fetch information for a non-existent track:
$ curl -i "https://api.spotify.com/v1/tracks/2KrxsD86ARO5beq7Q0Drfqa"

HTTP/1.1 400 Bad Request
{
    "error": {
        "status": 400,
        "message": "invalid id"
    }
}

Conditional Requests
Most API responses contain appropriate cache-control headers set to assist in client-side caching:
If you have cached a response, do not request it again until the response has expired.
If the response contains an ETag, set the If-None-Match request header to the ETag value.
If the response has not changed, the Spotify service responds quickly with 304 Not Modified status, meaning that your cached version is still good and your application should use it.
Timestamps
Timestamps are returned in ISO 8601 format as Coordinated Universal Time (UTC) with a zero offset: YYYY-MM-DDTHH:MM:SSZ. If the time is imprecise (for example, the date/time of an album release), an additional field indicates the precision; see for example, release_date in an Album Object.
Pagination
Some endpoints support a way of paging the dataset, taking an offset and limit as query parameters:
$ curl
https://api.spotify.com/v1/artists/1vCWHaC5f2uS3yhpwWbIA6/albums?album_type=SINGLE&offset=20&limit=10

In this example, in a list of 50 (total) singles by the specified artist : From the twentieth (offset) single, retrieve the next 10 (limit) singles.

## Authorization
Authorization refers to the process of granting a user or application access permissions to Spotify data and features (e.g your application needs permission from a user to access their playlists).
Spotify implements the OAuth 2.0 authorization framework:
Auth Intro
Where:
End User corresponds to the Spotify user. The End User grants access to the protected resources (e.g. playlists, personal information, etc.)
My App is the client that requests access to the protected resources (e.g. a mobile or web app).
Server which hosts the protected resources and provides authentication and authorization via OAuth 2.0.
The access to the protected resources is determined by one or several scopes. Scopes enable your application to access specific functionality (e.g. read a playlist, modify your library or just streaming) on behalf of a user. The set of scopes you set during the authorization, determines the access permissions that the user is asked to grant. You can find detailed information about scopes in the scopes documentation.
The authorization process requires valid client credentials: a client ID and a client secret. You can follow the Apps guide to learn how to generate them.
Once the authorization is granted, the authorization server issues an access token, which is used to make API calls on behalf the user or application.
The OAuth2 standard defines four grant types (or flows) to request and get an access token. Spotify implements the following ones:
Authorization code
Authorization code with PKCE extension
Client credentials
Implicit grant
Which OAuth flow should I use?
Choosing one flow over the rest depends on the application you are building:
If you are developing a long-running application (e.g. web app running on the server) in which the user grants permission only once, and the client secret can be safely stored, then the authorization code flow is the recommended choice.
In scenarios where storing the client secret is not safe (e.g. desktop, mobile apps or JavaScript web apps running in the browser), you can use the authorization code with PKCE, as it provides protection against attacks where the authorization code may be intercepted.
For some applications running on the backend, such as CLIs or daemons, the system authenticates and authorizes the app rather than a user. For these scenarios, Client credentials is the typical choice. This flow does not include user authorization, so only endpoints that do not request user information (e.g. user profile data) can be accessed.
The implicit grant has some important downsides: it returns the token in the URL instead of a trusted channel, and does not support refresh token. Thus, we don't recommend using this flow.
The following table summarizes the flows' behaviors:
FLOW	Access User Resources	Requires Secret Key (Server-Side)	Access Token Refresh
Authorization code	Yes	Yes	Yes
Authorization code with PKCE	Yes	No	Yes
Client credentials	No	Yes	No
Implicit grant	Yes	No	No


##Playlists
Playlists are containers for tracks and episodes. Spotify’s users have already created over 1.5 billion of them. By creating a playlist, a Spotify user can specify a subset of tracks and episodes; and the order in which to play them.
Through context menus and through support for drag-and-drop actions, the Spotify music players provide users with various controls for manually working with playlists. Playlists can be shared with, and followed by, other users, and they can be made available offline and used to seed other Spotify services, like radio.
playlist
Public, Private, and Collaborative Status
When creating or updating a playlist through the Spotify Web API, setting the attribute “public” to true will publish the playlist on the user’s profile, which means it will appear under “public playlists”. This will also make the playlist visible in search results.
A playlist created through the WebAPI will have the “public” attribute set to true by default and setting it to false does the opposite, it won’t be displayed on the user’s profile and won’t be visible through search results
Requests to these endpoints require different scopes depending on the status of this attribute, playlist-modify-public is required when setting it to true and playlist-modify-private when setting it to false. When creating a new playlist, the default value of the public attribute is true, which means unless this attribute is explicitly set to false, creating a playlist requires the playlist-modify-public scope.
Note that the public attribute does not refer to access control, modifying access is currently not possible through the WebAPI, so anyone with the link to the playlist can access it unless it’s made private through for instance the desktop client.
A playlist can also be made collaborative through the WebAPI, by setting the “collaborative” attribute to true. This means that anyone with the link can add to or remove a track from it. When creating a new playlist, the default value of the collaborative attribute is false
Note that this is slightly different from adding/removing collaborators, which is currently not possible through the WebAPI. You can read more about adding/removing collaborators here.
Furthermore, a playlist cannot have both the “collaborative” attribute and the “public” attribute set to true at the same time, so in order to set one of them to true the other must be set to false. Basically, a playlist cannot be both collaborative and published at the same time.
Reading a Playlist
To read a playlist, we first need to find it, and for that we need its Spotify ID. The Get a List of a User’s Playlists gives us an easy way to get basic details about a user’s playlists, including their IDs. This is, the playlists the user owns and the playlists the user is following, excluding collaborative playlists owned by other users. The set of playlists will be determined by the scopes granted to the application:
Owned and followed non-collaborative public playlists will be returned
Owned and followed non-collaborative private playlists will only be returned when the scope playlist-read-private has been granted
Owned and followed collaborative playlists will only be returned when the scope playlist-read-collaborative has been granted
Once we have a list of playlists we can retrieve the details of a specific playlist using the Web API’s Get a Playlist endpoint, and a list of its items using Get a Playlist’s Items. This last endpoint returns, in addition to an array of track and episode objects (depending on the additional_types parameter), information about who added the item and when it was added. (The items themselves are wrapped in a paging object to make it easy to retrieve very large playlists when necessary.)
Local Files
Spotify allows you to play your own collection of music files from within the Spotify client. These tracks appear alongside the music available on Spotify and can be included in users’ playlists, even if that particular track is not available on Spotify itself. For more information on local files, please read our support article.
The Web API can retrieve the contents of playlists, including information on any local files that have been added, via the Playlist endpoints.
Identifying Local Files
Requesting the contents of a playlist returns a set of track objects along with extra information about that track’s instance in the playlist. For example:
{
  "added_at": "2015-01-25T07:51:45Z",
  "added_by": {
    "external_urls": {
    "spotify": "http://open.spotify.com/user/exampleuser"
  },
  "href": "https://api.spotify.com/v1/users/exampleuser",
  "id": "exampleuser",
  "type": "user",
  "uri": "spotify:user:exampleuser"
},
"is_local": true,
"track": {
  [Spotify Track Object]
}

The key part here is the new property "is_local" which should be used to determine whether the track is a local file.
The Track Object for a Local File
The structure of a Spotify track object for a local file is identical to that of a regular Spotify track, with some notable differences in available data:
A number of fields will always be empty, zero, false or null
Some fields are populated from available local file information
The track URI has a special formatting
  "track": {
   "album": {
     "album_type": null,
     "available_markets": [],
     "external_urls": {},
     "href": null,
     "id": null,
     "images": [],
     "name": "Donkey Kong Country: Tropical Freeze",
     "type": "album",
     "uri": null
   },
   "artists": [
     {
       "external_urls": {},
       "href": null,
       "id": null,
       "name": "David Wise",
       "type": "artist",
       "uri": null
     }
   ],
   "available_markets": [],
   "disc_number": 0,
   "duration_ms": 127000,
   "explicit": false,
   "external_ids": {},
   "external_urls": {},
   "href": null,
   "id": null,
   "name": "Snomads Island",
   "popularity": 0,
   "preview_url": null,
   "track_number": 0,
   "type": "track",
   "uri": "spotify:local:David+Wise:Donkey+Kong+Country%3A+Tropical+Freeze:Snomads+Island:127"
 }
}

The local file information is read by the client software when the file was added to the playlist.
Although as much information as possible is taken from the local file, some may be missing so this information is not guaranteed to exist for all local files.
Understanding the Local File URI
The local file URI is constructed from information extracted from the local file when it was added to the playlist as follows:
spotify:local:{artist}:{album_title}:{track_title}:{duration_in_seconds}
All available information is also used to populate the object album name, artist name, track name and track duration properties, so parsing this directly should not be necessary.
How Should I Render Local Files to the User?
Whether you display these files to your app’s users is entirely dependent on the functionality that you require in your app. Initially, you could “grey out” the tracks or hide them altogether.
If you have access to the filesystem, you could use the information to match the track to the file and replicate the Spotify clients’ behaviour. Or perhaps use the title and artist information to perform a search in the Spotify catalogue.
Limitations
It is not currently possible to add local files to playlists using the Web API, but they can be Reordered or Removed. The latter should be done by specifying the index and snapshot_id, and NOT the URI of the track.
Folders
Folders are not returned through the Web API, nor can be created using it.
Version Control and Snapshots
The Web API provides several endpoints that allow playlists to be modified. These include Add Items to a Playlist, Remove Items from a Playlist, Replace a Playlist’s Items and Reorder a Playlist’s Items.
Every change to a playlist is saved in its version history. This makes possible features such as offline availability and collaborative editing, and restoring an accidentally removed playlist. Every time you add, remove, or move a track, your modification is applied on top of all previous modifications, causing the playlist to enter a new state known as a snapshot.
Spotify Playlists Version Control and Snapshots
If you need it, the Spotify Web API allows you to leverage snapshots to handle concurrent changes. Web API playlist endpoints like Create a Playlist and Get a Playlist, return a snapshot_id in the response body. This can be used later to identify the specific playlist version to target for changes when, for example, Removing Items from a Playlist. Concurrent changes are then automatically merged into the latest playlist version.
Following and Unfollowing a Playlist
Playlists can be followed or unfollowed programmatically through the Follow a Playlist and Unfollow a Playlist endpoints. Any playlist can be followed — public, private, and collaborative — provided you know the owner’s and the playlist’s Spotify IDs. When a user follows a playlist, the playlist’s owner will receive a notification in their Spotify client. When a track is added to a playlist, its followers will receive a notification in their Spotify client.
We have no endpoint for deleting a playlist in the Web API; the notion of deleting a playlist is not relevant within the Spotify’s playlist system. Even if you are the playlist’s owner and you choose to manually remove it from your own list of playlists, you are simply unfollowing it. Although this behavior may sound strange, it means that other users who are already following the playlist can keep enjoying it. Manually restoring a deleted playlist through the Spotify Accounts Service is the same thing as following one of your own playlists that you have previously unfollowed.
Using Playlist Images
Every playlist has an associated set of images which can be retrieved through Web API endpoints like Get a Playlist. In most cases there will be one image in a variety of sizes and the image will be a mosaic created from the album covers for the first few tracks:
cover-art-mosaic
The images array that’s returned can vary depending on how many tracks are in the playlist, and if the playlist has been manually “annotated”. The images array can contain:
Nothing, if the playlist has no tracks and is empty,
An album cover of size 640×640, if the playlist contains 1 to 3 tracks or has tracks from less than 4 different albums,
Three mosaic images of size 640×640, 300×300, and 60×60, if the playlist contains tracks from 4 or more albums,
A single custom image (example) in various sizes, if the playlist image has been set manually — for example, for some curated playlists.
The JSON returned by the Web API endpoints includes both the image dimensions (largest first) and a temporary link to the images:
...

"images" : [ {
"height" : 640,
"url" : "https://mosaic.scdn.co/640/e337f3661f68bc4d96a554de0ad7988d65edb25a134cd5ccaef9d411eba33df9542db9ba731aaf98ec04f9acee17a7576f939eb5aa317d20c6322494c4b4399d9b7c6f61b6a6ee70c616bc1a985c7ab8",
"width" : 640
}, {
"height" : 300,
"url" : "https://mosaic.scdn.co/300/e337f3661f68bc4d96a554de0ad7988d65edb25a134cd5ccaef9d411eba33df9542db9ba731aaf98ec04f9acee17a7576f939eb5aa317d20c6322494c4b4399d9b7c6f61b6a6ee70c616bc1a985c7ab8",
"width" : 300
}, {
"height" : 60,
"url" : "https://mosaic.scdn.co/60/e337f3661f68bc4d96a554de0ad7988d65edb25a134cd5ccaef9d411eba33df9542db9ba731aaf98ec04f9acee17a7576f939eb5aa317d20c6322494c4b4399d9b7c6f61b6a6ee70c616bc1a985c7ab8",
"width" : 60
} ],

...


Be aware that the links will expire in less than one day.
The use of album artwork in your applications is covered by our Developer Terms of Service. In particular you should be aware that:
You must display the album artwork in the form that we provide it (although you can resize it),
You should not store album artwork except when it is strictly necessary to operate your application, and
You must provide a link close to the cover art back to the full length track on Spotify. We provide design resources to help you with this.