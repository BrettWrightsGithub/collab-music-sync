# Authorization
var client = new HttpClient();
var request = new HttpRequestMessage(HttpMethod.Get, "https://api.spotify.com/v1/playlists/1DJxoWBdL48C5fm4PClrXj");
request.Headers.Add("Authorization", "Bearer BQDYqP7QuUgyLpwr_Zd2dcReS9W1GDayrtRELitFqrUPwSful1lKFk4_04LJAX09Yc0IX7kScK2dLKMVvaT0nY6ZPt5pHWC5HCFqw2mN33ce7i6uwgA");
var response = await client.SendAsync(request);
response.EnsureSuccessStatusCode();
Console.WriteLine(await response.Content.ReadAsStringAsync());


