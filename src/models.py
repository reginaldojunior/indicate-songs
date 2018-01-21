# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
	user = models.OneToOneField(User)
	url_image = models.CharField(max_length=150)
	access_token = models.CharField(max_length=255)


	class Meta:
		db_table = "user_profile"
		verbose_name = "user_profile"

class MusicIndicates(models.Model):
	url = models.CharField(max_length=150)
	to_user_id = models.IntegerField()
	from_user_id = models.IntegerField()
	image_album = models.CharField(max_length=150)
	track_name = models.CharField(max_length=100)


	class Meta:
		db_table = "music_indicates"

class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    music_indicates = models.ForeignKey(MusicIndicates, on_delete=models.CASCADE)
    text = models.TextField()
    date = models.CharField(max_length=10)
    time = models.CharField(max_length=10)


    class Meta:
    	db_table = "comments"