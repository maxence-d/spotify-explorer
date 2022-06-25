from django.db.models import Q
from django.http import Http404
from django.shortcuts import redirect
from .credentials import REDIRECT_URI, CLIENT_SECRET, CLIENT_ID

from rest_framework.views import APIView
from rest_framework.response import Response
from requests import Request, post

from .models import Artist, SpotifyToken
from .serializers import ArtistSerializer
from .utils import is_spotify_authenticated, get_user_tokens, execute_spotify_api_request, get_or_make_user_token
from rest_framework import status, authentication, permissions
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from django.utils import timezone
from datetime import timedelta


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


class SpFetchArtist(APIView, ):
    def get(self, request, sp_id, format=None):
        print(execute_spotify_api_request(f"artists/{sp_id}"))
        return Response()


class SpIsAuthenticated(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        is_authenticated = is_spotify_authenticated("AnonymousUser")
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
@api_view(('GET',))
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
        get_or_make_user_token("AnonymousUser",
                               response.get('access_token'),
                               response.get('token_type'),
                               response.get('expires_in'),
                               response.get('refresh_token')
                               )
    return redirect("http://localhost:8080/my-account")
