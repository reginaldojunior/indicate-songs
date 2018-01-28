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
	to_user_id = models.IntegerField(null=True)
	from_user_id = models.IntegerField(null=True)
	to_group_id = models.IntegerField(null=True)
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

class Group(models.Model):
	VISIBILITY = (
	    ('PUBLIC', 'PUBLIC'),
	    ('PRIVATE', 'PRIVATE'),
	    ('SECRET', 'SECRET'),
	)

	name = models.CharField(max_length=200)
	description = models.TextField()
	visibility = models.CharField(max_length=10, choices=VISIBILITY)
	owner = models.ForeignKey(User, on_delete=models.CASCADE)


	class Meta:
		db_table = "group"


class GroupAdmins(models.Model):
	PERMISSION = (
		('ADMIN', 'ADMIN'),
		('MODERATOR', 'MODERATOR')
	)

	user = models.ForeignKey(User, on_delete=models.CASCADE)
	group = models.ForeignKey(Group, on_delete=models.CASCADE)
	permission = models.CharField(max_length=15, choices=PERMISSION)


	class Meta:
		db_table = "group_admins"
