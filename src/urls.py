from django.conf.urls import include, url
from django.contrib import admin

from . import views

urlpatterns = [
	url(r'^search/friend$', views.get_friends_by_keywords, name='get_friends_by_keywords'),
	url(r'^search/music$', views.get_musics_by_keywords, name='get_musics_by_keywords'),
	url(r'^indicate/music$', views.post_indicate_music, name='post_indicate_music'),
	url(r'^music/comment$', views.post_music_comment, name='post_music_comment'),
    url(r'^groups$', views.groups, name='groups'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^auth_spotify/$', views.auth_spotify, name='auth_spotify'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^music_indicates$', views.music_indicates, name='music_indicates'),
    url(r'^indicates$', views.indicates, name='indicates'),
    url(r'^$', views.home, name='home'),
]
