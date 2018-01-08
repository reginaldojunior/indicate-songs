import spotipy
from spotipy import oauth2

PORT_NUMBER = 8000
SPOTIPY_CLIENT_ID = '126336c473d64c0ba869e44b7c0ec8b7'
SPOTIPY_CLIENT_SECRET = 'e5398244b9a842018d401754397e4f43'
SPOTIPY_REDIRECT_URI = 'http://localhost:8000'
SCOPE = 'user-library-read'
CACHE = '.spotipyoauthcache'

sp_oauth = oauth2.SpotifyOAuth( 
	SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, 
	SPOTIPY_REDIRECT_URI, scope=SCOPE, cache_path=CACHE
)

print sp_oauth

# spotify = spotipy.Spotify()
# results = spotify.search(q='artist: Racionais MC\'s', type='artist')

# print results