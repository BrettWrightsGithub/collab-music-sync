from: https://unofficial-google-music-api.readthedocs.io/en/latest/reference/musicmanager.html#setup-and-login


The google play music api access will be acheived through this github repo: [https://github.com/simon-weber/gmusicapi(https://github.com/simon-weber/gmusicapi)

Here's the ReadMe
gmusicapi: an unofficial API for Google Play Music
gmusicapi allows control of Google Music with Python.

from gmusicapi import Mobileclient

api = Mobileclient()
# after running api.perform_oauth() once:
api.oauth_login('<a previously-registered device id>')
# => True

library = api.get_all_songs()
sweet_track_ids = [track['id'] for track in library
                   if track['artist'] == 'The Cat Empire']

playlist_id = api.create_playlist('Rad muzak')
api.add_songs_to_playlist(playlist_id, sweet_track_ids)
gmusicapi is not supported nor endorsed by Google.

That said, it's actively maintained, and powers a bunch of cool projects:

alternate clients, including one designed for the visually impaired, a web-based jukebox which ships with its own server, command line clients, a FUSE filesystem, and an Alexa skill
library management tools for syncing tracks, syncing playlists, and migrating to a different account
proxies for media players, such as gmusicproxy and gmusicprocurator, as well as plugins for Mopidy, Squeezebox and Tizonia.
enhancements like autoplaylists / smart playlists
Getting started

Start with the usage docs, which will guide you through installation and the available apis.

Once you're up and running, you can explore the rest of the docs at http://unofficial-google-music-api.readthedocs.io.

If the documentation doesn't answer your questions, or you just want to get in touch, either drop by #gmusicapi on Freenode or shoot me an email.

Status and updates

build_status

January 2020: Python 2 support dropped.
November 2018: proper OAuth support for the mobileclient.
February 2016: Python 3 support!
September 2015: Google switched to a new music uploading endpoint, breaking uploading for outdated versions of gmusicapi.
June 2015: Full mobileclient and webclient functionality was restored.
May 2015: Limited mobileclient functionality was restored.
April 2015: Google deprecated clientlogin, breaking both the webclient and mobileclient.
November 2013: I started working fulltime at Venmo, meaning this project is back to night and weekend development.
For fine-grained development updates, follow me on Twitter: @simonmweber.


Usage

Installation

Use pip: $ pip install gmusicapi.

To install the yet-to-be-released development version, use $ pip install git+https://github.com/simon-weber/gmusicapi.git@develop#egg=gmusicapi.

If you’re going to be uploading music, you’ll likely need avconv or ffmpeg installed and in your system path, along with at least libmp3lame:

Linux
Use your distro’s package manager: e.g $ sudo apt-get install libav-tools libavcodec-extra-53 (ffmpeg requires extra steps on Debian/Ubuntu).
Download pre-built binaries of avconv or ffmpeg and edit your path to include the directory that contains avconv/ffmpeg.
Mac
Use Homebrew to install libav (avconv) or ffmpeg.
Windows
Download pre-built binaries of avconv or ffmpeg and edit your path to include the directory that contains avconv.exe/ffmpeg.exe.
Google App Engine
See this thread for instructions.
The only time avconv or ffmpeg is not required is when uploading mp3s without scan-and-match enabled.

If you need to install avconv/ffmpeg from source, be sure to use $ ./configure --enable-gpl --enable-nonfree --enable-libmp3lame.

Quickstart

There are two supported client classes based on different Google apis.

The Mobileclient uses the Android app’s apis to handle library management and playback.

The Musicmanager uses the desktop Music Manager’s apis to handle uploading and downloading.

Both have similar command-line OAuth2 interfaces for logging in. For example:

from gmusicapi import Musicmanager

mm = Musicmanager()
mm.perform_oauth()
This only needs to be run once, and if successful will save a refresh token to disk. Then, future runs can start with:

from gmusicapi import Musicmanager

mm = Musicmanager()
mm.login()  # currently named oauth_login for the Mobileclient
If you need both library management and uploading, just create multiple client instances.

There is also the Webclient, which is uses the webapp’s apis to handle similar tasks to the Mobileclient. It is not tested nor well supported, and requires providing full account credentials to use. Avoid it if possible.

The reference section has complete information on all clients:

Client Interfaces
Webclient Interface
Mobileclient Interface
Musicmanager Interface
Setup and login

classmethod Musicmanager.perform_oauth(storage_filepath=<object object>, open_browser=False)
Provides a series of prompts for a user to follow to authenticate. Returns oauth2client.client.OAuth2Credentials when successful.

In most cases, this should only be run once per machine to store credentials to disk, then never be needed again.

If the user refuses to give access, oauth2client.client.FlowExchangeError is raised.

Parameters:	
storage_filepath –
a filepath to write the credentials to, or None to not write the credentials to disk (which is not recommended).

Appdirs user_data_dir is used by default. Check the OAUTH_FILEPATH field on this class to see the exact location that will be used.

open_browser – if True, attempt to open the auth url in the system default web browser. The url will be printed regardless of this param’s setting.
This flow is intentionally very simple. For complete control over the OAuth flow, pass an oauth2client.client.OAuth2Credentials to login() instead.

Musicmanager.__init__(debug_logging=True, validate=True, verify_ssl=True)
Parameters:	
debug_logging –
each Client has a logger member. The logger is named gmusicapi.<client class><client number> and will propogate to the gmusicapi root logger.

If this param is True, handlers will be configured to send this client’s debug log output to disk, with warnings and above printed to stderr. Appdirs user_log_dir is used by default. Users can run:

from gmusicapi.utils import utils
print utils.log_filepath
to see the exact location on their system.

If False, no handlers will be configured; users must create their own handlers.

Completely ignoring logging is dangerous and not recommended. The Google Music protocol can change at any time; if something were to go wrong, the logs would be necessary for recovery.

validate –
if False, do not validate server responses against known schemas. This helps to catch protocol changes, but requires significant cpu work.

This arg is stored as self.validate and can be safely modified at runtime.

verify_ssl – if False, exceptions will not be raised if there are problems verifying SSL certificates. Be wary of using this option; it’s almost always better to fix the machine’s SSL configuration than to ignore errors.
Musicmanager.login(oauth_credentials='/home/docs/.local/share/gmusicapi/oauth.cred', uploader_id=None, uploader_name=None)
Authenticates the Music Manager using OAuth. Returns True on success, False on failure.

Unlike the Webclient, OAuth allows authentication without providing plaintext credentials to the application.

In most cases, the default parameters should be acceptable. Users on virtual machines will want to provide uploader_id.

Parameters:	
oauth_credentials –
oauth2client.client.OAuth2Credentials or the path to a oauth2client.file.Storage file. By default, the same default path used by perform_oauth() is used.

Endusers will likely call perform_oauth() once to write credentials to disk and then ignore this parameter.

This param is mostly intended to allow flexibility for developers of a 3rd party service who intend to perform their own OAuth flow (eg on their website).

uploader_id –
a unique id as a MAC address, eg '00:11:22:33:AA:BB'. This should only be provided in cases where the default (host MAC address incremented by 1) will not work.

Upload behavior is undefined if a Music Manager uses the same id, especially when reporting bad matches.

ValueError will be raised if this is provided but not in the proper form.

OSError will be raised if this is not provided and a real MAC could not be determined (most common when running on a VPS).

If provided, use the same id on all future runs for this machine, because of the upload device limit explained below.

uploader_name –
human-readable non-unique id; default is "<hostname> (gmusicapi-{version})".

This doesn’t appear to be a part of authentication at all. Registering with (id, name = X, Y) and logging in with (id, name = X, Z) works, and does not change the server-stored uploader_name.

There are hard limits on how many upload devices can be registered; refer to Google’s docs. There have been limits on deauthorizing devices in the past, so it’s smart not to register more devices than necessary.

Musicmanager.logout(revoke_oauth=False)
Forgets local authentication in this Client instance.

Parameters:	revoke_oauth – if True, oauth credentials will be permanently revoked. If credentials came from a file, it will be deleted.
Returns True on success.

Uploading Songs

Musicmanager.upload(filepaths, enable_matching=False, enable_transcoding=True, transcode_quality='320k')
Uploads the given filepaths.

All non-mp3 files will be transcoded before being uploaded. This is a limitation of Google’s backend.

An available installation of ffmpeg or avconv is required in most cases: see the installation page for details.

Returns a 3-tuple (uploaded, matched, not_uploaded) of dictionaries, eg:

(
    {'<filepath>': '<new server id>'},               # uploaded
    {'<filepath>': '<new server id>'},               # matched
    {'<filepath>': '<reason, eg ALREADY_EXISTS>'}    # not uploaded
)
Parameters:	
filepaths – a list of filepaths, or a single filepath.
enable_matching – if True, attempt to use scan and match to avoid uploading every song. This requires ffmpeg or avconv. WARNING: currently, mismatched songs can not be fixed with the ‘Fix Incorrect Match’ button nor report_incorrect_match. They would have to be deleted and reuploaded with matching disabled (or with the Music Manager). Fixing matches from gmusicapi may be supported in a future release; see issue #89.
enable_transcoding – if False, non-MP3 files that aren’t matched using scan and match will not be uploaded.
transcode_quality – if int, pass to ffmpeg/avconv -q:a for libmp3lame (lower-better int,). If string, pass to ffmpeg/avconv -b:a (eg '128k' for an average bitrate of 128k). The default is 320kbps cbr (the highest possible quality).
All Google-supported filetypes are supported; see Google’s documentation.

If PERMANENT_ERROR is given as a not_uploaded reason, attempts to reupload will never succeed. The file will need to be changed before the server will reconsider it; the easiest way is to change metadata tags (it’s not important that the tag be uploaded, just that the contents of the file change somehow).

Downloading Songs

Musicmanager.get_uploaded_songs(incremental=False)
Returns a list of dictionaries, each with the following keys: ('id', 'title', 'album', 'album_artist', 'artist', 'track_number', 'track_size', 'disc_number', 'total_disc_count').

All Access tracks that were added to the library will not be included, only tracks uploaded/matched by the user.

Parameters:	incremental – if True, return a generator that yields lists of at most 1000 dictionaries as they are retrieved from the server. This can be useful for presenting a loading bar to a user.
Musicmanager.get_purchased_songs(incremental=False)
Returns a list of dictionaries, each with the following keys: ('id', 'title', 'album', 'album_artist', 'artist', 'track_number', 'track_size', 'disc_number', 'total_disc_count').

Parameters:	incremental – if True, return a generator that yields lists of at most 1000 dictionaries as they are retrieved from the server. This can be useful for presenting a loading bar to a user.
Musicmanager.download_song(song_id)
Download an uploaded or purchased song from your library.

Subscription tracks can’t be downloaded with this method.

Returns a tuple (u'suggested_filename', 'audio_bytestring'). The filename will be what the Music Manager would save the file as, presented as a unicode string with the proper file extension. You don’t have to use it if you don’t want.

Parameters:	song_id – a single uploaded or purchased song id.
To write the song to disk, use something like:

filename, audio = mm.download_song(an_id)

# if open() throws a UnicodeEncodeError, either use
#   filename.encode('utf-8')
# or change your default encoding to something sane =)
with open(filename, 'wb') as f:
    f.write(audio)
Unlike with Webclient.get_song_download_info, there is no download limit when using this interface.

Also unlike the Webclient, downloading a track requires authentication. Returning a url does not suffice, since retrieving a track without auth will produce an http 500.

Misc

..automethod:: Musicmanager.get_quota