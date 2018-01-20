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