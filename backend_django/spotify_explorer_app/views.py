from django.db.models import Q
from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Artist
from .serializers import ArtistSerializer


class ArtistDetail(APIView):
    def get_object(self, sp_id):
        try:
            return Artist.objects.get(sp_id=sp_id)
        except Artist.DoesNotExist:
            raise Http404
    
    def get(self, request, sp_id, format=None):
        artist = self.get_object(sp_id)
        serializer = ArtistSerializer(artist)
        return Response(serializer.data)
