
import spotipy

from spotipy import oauth2
from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from models import UserProfile


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

def signup(request):
	auth_url = getSPOauthURI()

	return render(request, 'signup.html', {'auth_url': auth_url})

def home(request):
	access_token = None

	if 'access_token' in request.session:
		access_token = request.session['access_token']
	
	if request.GET['code'] and access_token is None:
		token_info = sp_oauth.get_access_token(request.GET['code'])
		access_token = token_info['access_token']

	try:
		sp = spotipy.Spotify(auth=access_token)
		user = sp.current_user()
	except Exception, e:
		return redirect('signup')

	try:
		user_exist = User.objects.get(username=user['uri'])
	except Exception, e:
		user_exist = None

	if not user_exist:
		UserModel = User.objects.create_user(
			user['uri'], first_name=user['display_name']
		).save()

		user_profile = UserProfile(
			user_id=User.objects.last().id,
			access_token=access_token,
			url_image=user['images'][0]['url']
		).save()

		user_exist = User.objects.last()

	request.session['user_id'] = user_exist.id
	request.session['access_token'] = access_token

	return render(request, 'home.html', {
		'user': user,
		'access_token': access_token,
		'error': None
	})

def getSPOauthURI():	
	auth_url = sp_oauth.get_authorize_url()

	return auth_url

def auth_spotify(request):
	return render(request, 'auth_spotify.html', {'auth': sp_oauth})