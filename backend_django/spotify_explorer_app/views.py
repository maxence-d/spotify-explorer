from django.db.models import Q
from django.http import Http404
from .credentials import REDIRECT_URI, CLIENT_SECRET, CLIENT_ID

from rest_framework.views import APIView
from rest_framework.response import Response
from requests import Request, post

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


class SpIsAuthenticated(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        sp_token = SpotifyToken.objects.filter(user=request.user).first()
        is_authenticated = is_spotify_authenticated(sp_token)
        return Response({'sp_is_auth': is_authenticated}, status=status.HTTP_200_OK)

class SpGetAuthURL(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, format=None):
        scopes = 'user-read-playback-state user-modify-playback-state user-read-currently-playing'

        url = Request('GET', 'https://accounts.spotify.com/authorize', params={
            'scope': scopes,
            'response_type': 'code',
            'redirect_uri': REDIRECT_URI,
            'client_id': CLIENT_ID
        }).prepare().url

        return Response({'url': url}, status=status.HTTP_200_OK)


@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def spotify_callback(request, format=None):
    code = request.GET.get('code')
    error = request.GET.get('error')

    response = post('https://accounts.spotify.com/api/token', data={
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }).json()

    error = response.get('error')
    if not error:
        sp_token = SpotifyToken(
            user=request.user, 
            access_token=response.get('access_token'),
            refresh_token=response.get('refresh_token'), 
            token_type=response.get('token_type'), 
            expires_in=response.get('expires_in')
        )
        sp_token.save()
        return Response({'status': True}, status=status.HTTP_200_OK)
    else:
        return Response({'status': False}, status=status.HTTP_400_BAD_REQUEST)
