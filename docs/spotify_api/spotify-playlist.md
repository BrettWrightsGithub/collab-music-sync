https://developer.spotify.com/documentation/web-api/reference/get-playlist

Get Playlist


OAuth 2.0
Get a playlist owned by a Spotify user.

Important policy notes
Spotify content may not be downloaded
Keep visual content in its original form
Ensure content attribution
Spotify content may not be used to train machine learning or AI model
Request

GET
/playlists/{playlist_id}
playlist_id
string
Required
The Spotify ID of the playlist.
Example: 3cEYpjA9oz9GiPac4AsH4n
market
string
An ISO 3166-1 alpha-2 country code. If a country code is specified, only content that is available in that market will be returned.
If a valid user access token is specified in the request header, the country associated with the user account will take priority over this parameter.
Note: If neither market or user country are provided, the content is considered unavailable for the client.
Users can view the country that is associated with their account in the account settings.
Example: market=ES
fields
string
Filters for the query: a comma-separated list of the fields to return. If omitted, all fields are returned. For example, to get just the playlist''s description and URI: fields=description,uri. A dot separator can be used to specify non-reoccurring fields, while parentheses can be used to specify reoccurring fields within objects. For example, to get just the added date and user ID of the adder: fields=tracks.items(added_at,added_by.id). Use multiple parentheses to drill down into nested objects, for example: fields=tracks.items(track(name,href,album(name,href))). Fields can be excluded by prefixing them with an exclamation mark, for example: fields=tracks.items(track(name,href,album(!name,href)))
Example: fields=items(added_by.id,track(name,href,album(name,href)))
additional_types
string
A comma-separated list of item types that your client supports besides the default track type. Valid types are: track and episode.
Note: This parameter was introduced to allow existing clients to maintain their current behaviour and might be deprecated in the future.
In addition to providing this parameter, make sure that your client properly handles cases of new types in the future by checking against the type field of each object.
Response
200
401
403
429
A playlist
collaborative
boolean
true if the owner allows other users to modify the playlist.
description
string
Nullable
The playlist description. Only returned for modified, verified playlists, otherwise null.

external_urls
object
Known external URLs for this playlist.
spotify
string
The Spotify URL for the object.

followers
object
Information about the followers of the playlist.
href
string
Nullable
This will always be set to null, as the Web API does not support it at the moment.
total
integer
The total number of followers.
href
string
A link to the Web API endpoint providing full details of the playlist.
id
string
The Spotify ID for the playlist.

images
array of ImageObject
Images for the playlist. The array may be empty or contain up to three images. The images are returned by size in descending order. See Working with Playlists. Note: If returned, the source URL for the image (url) is temporary and will expire in less than a day.
url
string
Required
The source URL of the image.
Example: "https://i.scdn.co/image/ab67616d00001e02ff9ca10b55ce82ae553c8228"
height
integer
Required
Nullable
The image height in pixels.
Example: 300
width
integer
Required
Nullable
The image width in pixels.
Example: 300
name
string
The name of the playlist.

owner
object
The user who owns the playlist

external_urls
object
Known public external URLs for this user.

followers
object
Information about the followers of this user.
href
string
A link to the Web API endpoint for this user.
id
string
The Spotify user ID for this user.
type
string
The object type.
Allowed values: "user"
uri
string
The Spotify URI for this user.
display_name
string
Nullable
The name displayed on the user's profile. null if not available.
public
boolean
The playlist's public/private status (if it is added to the user's profile): true the playlist is public, false the playlist is private, null the playlist status is not relevant. For more about public/private status, see Working with Playlists
snapshot_id
string
The version identifier for the current playlist. Can be supplied in other requests to target a specific playlist version

tracks
object
The tracks of the playlist.
href
string
Required
A link to the Web API endpoint returning the full result of the request
Example: "https://api.spotify.com/v1/me/shows?offset=0&limit=20"
limit
integer
Required
The maximum number of items in the response (as set in the query or by default).
Example: 20
next
string
Required
Nullable
URL to the next page of items. ( null if none)
Example: "https://api.spotify.com/v1/me/shows?offset=1&limit=1"
offset
integer
Required
The offset of the items returned (as set in the query or by default)
Example: 0
previous
string
Required
Nullable
URL to the previous page of items. ( null if none)
Example: "https://api.spotify.com/v1/me/shows?offset=1&limit=1"
total
integer
Required
The total number of items available to return.
Example: 4

items
array of PlaylistTrackObject
Required
type
string
The object type: "playlist"
uri
string
The Spotify URI for the playlist.


