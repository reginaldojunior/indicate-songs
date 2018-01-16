from django.conf.urls import include, url
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^auth_spotify/$', views.auth_spotify, name='auth_spotify'),
    url(r'^$', views.home, name='home'),
]
