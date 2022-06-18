from rest_framework import serializers

from .models import Artist

class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = (
            "id",
            "sp_id",
            "name",
            "get_absolute_url",
            "get_image",
            "get_thumbnail"
        )

