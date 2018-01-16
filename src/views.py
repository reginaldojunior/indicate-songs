
from django.shortcuts import render
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

# Create your views here.
def home(request):
	auth_url = getSPOauthURI()
	access_token = ''
    
	try:
		if request.GET['code']:
			token_info = sp_oauth.get_access_token(request.GET['code'])
			access_token = token_info['access_token']

			sp = spotipy.Spotify(auth=access_token)
			results = sp.current_user_saved_tracks()

			print results
	except Exception, e:
		return render(request, 'home.html', {'auth_url': auth_url, 'access_token': access_token, 'error': e})


	return render(request, 'home.html', {'auth_url': auth_url, 'access_token': access_token, 'error': None})

def getSPOauthURI():	
	auth_url = sp_oauth.get_authorize_url()

	return auth_url

def auth_spotify(request):
	return render(request, 'auth_spotify.html', {'auth': sp_oauth})