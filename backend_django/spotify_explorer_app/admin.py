from django.contrib import admin

from .models import Artist, SpotifyToken

admin.site.register(Artist)
admin.site.register(SpotifyToken)