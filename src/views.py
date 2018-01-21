
import spotipy

from spotipy import oauth2
from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from django.http import JsonResponse
from models import UserProfile, MusicIndicates


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
	
	if 'code' in request.GET:
		if request.GET['code'] and access_token is None:
			token_info = sp_oauth.get_access_token(request.GET['code'])
			access_token = token_info['access_token']

	try:
		sp = spotipy.Spotify(auth=access_token)
		user = sp.current_user()
	except Exception, e:
		del request.session['access_token']

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
		'error': None,
		'home': True
	})

def music_indicates(request):
	access_token = request.session['access_token']
	
	sp = spotipy.Spotify(auth=access_token)
	user = sp.current_user()

	musics = MusicIndicates.objects.filter(from_user_id=request.session['user_id'])

	result = []
	for music in musics:
		to_user = User.objects.get(id=music.to_user_id)
		to_user_profile = UserProfile.objects.get(user_id=music.to_user_id)

		result.append({
			'url': music.url,
			'image_album': music.image_album,
			'track_name': music.track_name,
			'to_user_name': to_user.first_name,
			'to_user_url_image': to_user_profile.url_image
		})

	return render(request, 'music_indicates.html', {
		'musics': result,
		'user': user,
		'access_token': access_token,
		'error': None,
		'music_indicates': True
	})

def indicates(request):
	access_token = request.session['access_token']
	
	sp = spotipy.Spotify(auth=access_token)
	user = sp.current_user()

	musics = MusicIndicates.objects.filter(to_user_id=request.session['user_id'])

	result = []
	for music in musics:
		from_user = User.objects.get(id=music.from_user_id)
		from_user_profile = UserProfile.objects.get(user_id=music.from_user_id)

		result.append({
			'url': music.url,
			'image_album': music.image_album,
			'track_name': music.track_name,
			'from_user_name': from_user.first_name,
			'from_user_url_image': from_user_profile.url_image
		})

	return render(request, 'indicates.html', {
		'musics': result,
		'user': user,
		'access_token': access_token,
		'indicates': True
	})

@csrf_exempt
def get_friends_by_keywords(request):
	users = User.objects.filter(first_name__contains=request.POST['name'])

	response = []
	for user in users:
		user_profile = UserProfile.objects.get(user_id=user.id)

		response.append({
			'id': user.id,
			'name': user.first_name,
			'url_image': user_profile.url_image,
			'access_token': user_profile.access_token
		})

	return JsonResponse({'users': response})

@csrf_exempt
def get_musics_by_keywords(request):
	access_token = request.session['access_token']
	sp = spotipy.Spotify(auth=access_token)

	tracks = sp._get('https://api.spotify.com/v1/search?q=' + request.POST['term'] + '&type=track')
	
	return JsonResponse(tracks)

@csrf_exempt
def post_indicate_music(request):
	Music = MusicIndicates(
		url=request.POST['url'],
		to_user_id=request.POST['to_user_id'],
		from_user_id=request.session['user_id'],
		image_album=request.POST['image_album'],
		track_name=request.POST['track_name']
	)

	Music.save()

	return JsonResponse({})

def getSPOauthURI():	
	auth_url = sp_oauth.get_authorize_url()

	return auth_url

def auth_spotify(request):
	return render(request, 'auth_spotify.html', {'auth': sp_oauth})