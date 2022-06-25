from io import BytesIO
from django.contrib.auth.models import User
from PIL import Image
from django.db import models


class Artist(models.Model):
    name = models.CharField(max_length=255)
    sp_id = models.CharField(max_length=255, primary_key=True)
    followers = models.IntegerField()
    following = models.ManyToManyField(User, default=None)
    image_url = models.URLField(default='')

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return f"{self.name} ({self.sp_id})"

    def get_absolute_url(self):
        return f'/artist/{self.sp_id}/'


class SpotifyToken(models.Model):
    user = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    refresh_token = models.CharField(max_length=150)
    access_token = models.CharField(max_length=150)
    expires_in = models.DateTimeField()
    token_type = models.CharField(max_length=50)

    @classmethod
    def create(cls, user, refresh_token, access_token, expires_in, token_type):
        return cls(user=user, refresh_token=refresh_token, access_token=access_token, expires_in=expires_in,
                   token_type=token_type)

    def __str__(self):
        return f"{self.user} ({self.created_at}) ({self.refresh_token}) ({self.access_token}) ({self.expires_in}) ({self.token_type})"
