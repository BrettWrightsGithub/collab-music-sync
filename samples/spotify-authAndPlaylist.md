# Authorization
var client = new HttpClient();
var request = new HttpRequestMessage(HttpMethod.Get, "https://api.spotify.com/v1/playlists/1DJxoWBdL48C5fm4PClrXj");
request.Headers.Add("Authorization", "Bearer BQDYqP7QuUgyLpwr_Zd2dcReS9W1GDayrtRELitFqrUPwSful1lKFk4_04LJAX09Yc0IX7kScK2dLKMVvaT0nY6ZPt5pHWC5HCFqw2mN33ce7i6uwgA");
var response = await client.SendAsync(request);
response.EnsureSuccessStatusCode();
Console.WriteLine(await response.Content.ReadAsStringAsync());

## response
{
    "access_token": "BQD9jB8CfHm26mkDg4axge90VKFEIjd-qfOa-v3KjawF65vqaDZcD2qAf8-8TkSfwa3cJQq0IrVbdD2r6nP4JisXf-fxPMS2X_zhOnSA-8J7h1A1BqA",
    "token_type": "Bearer",
    "expires_in": 3600
}


# Playlist
var client = new HttpClient();
var request = new HttpRequestMessage(HttpMethod.Get, "https://api.spotify.com/v1/playlists/7k5RPyBSipddoxXg03bs7J/tracks");
request.Headers.Add("Authorization", "Bearer BQD9jB8CfHm26mkDg4axge90VKFEIjd-qfOa-v3KjawF65vqaDZcD2qAf8-8TkSfwa3cJQq0IrVbdD2r6nP4JisXf-fxPMS2X_zhOnSA-8J7h1A1BqA");
var response = await client.SendAsync(request);
response.EnsureSuccessStatusCode();
Console.WriteLine(await response.Content.ReadAsStringAsync());


## playlist reponse

| **Field**              | **JSON Path**                                                  | **Notes**                                                                                                                                                                                                              |
|------------------------|----------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Playlist Items         | `items`                                                        | An array of all playlist entries (each entry has `added_at`, `added_by`, `track`, etc.).                                                                                                                               |
| Added At               | `items[*].added_at`                                            | Timestamp indicating when the track was added to the playlist.                                                                                                                                                         |
| Added By (User)        | `items[*].added_by.id`                                         | The Spotify user ID of the person who added the track.                                                                                                                                                                 |
| Is Local Track Flag    | `items[*].is_local`                                            | `true` if track is a local file instead of a Spotify track. Typically `false` for standard Spotify tracks.                                                                                                             |
| Track ID               | `items[*].track.id`                                            | The Spotify track’s unique ID.                                                                                                                                                                                         |
| Track URI              | `items[*].track.uri`                                           | The Spotify track’s URI (format: `spotify:track:<id>`).                                                                                                                                                               |
| Track Name             | `items[*].track.name`                                          | The display name of the song.                                                                                                                                                                                          |
| Track Duration (ms)    | `items[*].track.duration_ms`                                   | Duration of the track in milliseconds.                                                                                                                                                                                 |
| Track Preview URL      | `items[*].track.preview_url`                                   | A short preview audio clip URL (if available).                                                                                                                                                                         |
| Track External URLs    | `items[*].track.external_urls.spotify`                         | Spotify web URL for the track.                                                                                                                                                                                         |
| Album ID               | `items[*].track.album.id`                                      | The Spotify album’s unique ID.                                                                                                                                                                                         |
| Album Name             | `items[*].track.album.name`                                    | The album’s title.                                                                                                                                                                                                     |
| Album Release Date     | `items[*].track.album.release_date`                            | Release date of the album (format can be day, month, or year precision).                                                                                                                                                |
| Album Images           | `items[*].track.album.images`                                  | Array of album art objects, each containing `url`, `height`, `width`.                                                                                                                                                  |
| Artist(s) Array        | `items[*].track.artists`                                      | An array of artist objects for the track.                                                                                                                                                                              |
| Artist ID(s)           | `items[*].track.artists[*].id`                                 | Each artist’s unique ID.                                                                                                                                                                                               |
| Artist Name(s)         | `items[*].track.artists[*].name`                               | Each artist’s display name.                                                                                                                                                                                            |
| Disc Number            | `items[*].track.disc_number`                                   | The disc number (typically 1) on multi-disc albums.                                                                                                                                                                    |
| Track Number           | `items[*].track.track_number`                                  | The track’s position on the album.                                                                                                                                                                                     |
| External IDs (e.g. ISRC)| `items[*].track.external_ids.isrc`                             | Identifiers like an ISRC code if you need cross-referencing.                                                                                                                                                           |
| Markets                | `items[*].track.available_markets`                             | List of country codes where this track is playable.                                                                                                                                                                    |
| Primary Color          | `items[*].primary_color`                                       | May be `null`; sometimes used in Spotify’s own UI for brand coloring.                                                                                                                                                  |
| Video Thumbnail        | `items[*].video_thumbnail.url`                                 | May be `null`; only applies if the track has a video or canvas.                                                                                                                                                        |
| Pagination Info        | `href`, `limit`, `next`, `offset`, `previous`, `total`         | Top-level fields for pagination and references (not strictly required for track-level sync, but can be useful to handle large playlists).                                                                              |

What You’ll Typically Use in a Sync
	1.	Track ID / URI – Critical for referencing which song to add or remove in another service.
	2.	Track Name, Artist(s), and Album – Used for matching or searching on other platforms.
	3.	Added At – Helps track ordering or which tracks were added recently.
	4.	Added By – Useful if you care about who added the track (not always needed for a basic sync).