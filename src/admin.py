from django.contrib import admin
from .models import UserProfile, MusicIndicates, Comments

admin.site.register(UserProfile)
admin.site.register(MusicIndicates)
admin.site.register(Comments)