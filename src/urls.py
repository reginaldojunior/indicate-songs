from django.conf.urls import include, url
from django.contrib import admin

from . import views

urlpatterns = [
	url(r'^search/friend$', views.get_friends_by_keywords, name='get_friends_by_keywords'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^auth_spotify/$', views.auth_spotify, name='auth_spotify'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^$', views.home, name='home'),
]
