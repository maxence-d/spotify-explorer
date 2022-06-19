from django.db.models import Q
from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Artist, SpotifyToken
from .serializers import ArtistSerializer
from .utils import is_spotify_authenticated
from rest_framework import status, authentication, permissions
from rest_framework.decorators import api_view, authentication_classes, permission_classes


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


class ArtistList(APIView):
    def get(self, request, format=None):
        artists = Artist.objects.all()
        serializer = ArtistSerializer(artists, many=True)
        return Response(serializer.data)



class IsAuthenticated(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        sp_token = SpotifyToken.objects.filter(user=request.user).first()
        is_authenticated = is_spotify_authenticated(sp_token)
        return Response({'sp_is_auth': is_authenticated}, status=status.HTTP_200_OK)

