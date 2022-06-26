from django.contrib import admin

from .models import Artist, SpotifyToken, CustomUser

admin.site.register(Artist)
admin.site.register(SpotifyToken)
admin.site.register(CustomUser)
