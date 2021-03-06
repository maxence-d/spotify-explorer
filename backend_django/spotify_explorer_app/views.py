import json
from pprint import pprint

from django.http import Http404
from django.shortcuts import redirect
from requests import Request, post
from rest_framework import status, authentication, permissions
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView

from .credentials import REDIRECT_URI, CLIENT_SECRET, CLIENT_ID
from .model_utils import get_or_make_artist_from_sp, update_following
from .models import Artist, CustomUser
from .serializers import ArtistSerializer, CustomUserSerializer
from .utils import is_spotify_authenticated, execute_spotify_api_request, get_or_make_user_token, remove_user_tokens


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


class UserFollowingList(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        user = CustomUser.objects.get(user=request.user)
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)


class SpFetchAlbums(APIView):
    def get(self, request, sp_id, format=None):
        response, code = execute_spotify_api_request(f"artists/{sp_id}/albums")
        if code.status_code == status.HTTP_200_OK:
            return Response({'sp_albums': response}, status=code.status_code)
        else:
            return Response({'error': response}, status=code.status_code)

class SpFetchArtist(APIView):
    def get(self, request, sp_id, format=None):
        response, code = execute_spotify_api_request(f"artists/{sp_id}")
        if code.status_code == status.HTTP_200_OK:
            get_or_make_artist_from_sp(sp_id, response)
            return Response({'sp_artist': response}, status=code.status_code)
        else:
            return Response({'error': response}, status=code.status_code)


class SpFetchFollowing(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        response, code = execute_spotify_api_request(f"me/following?type=artist")
        if code.status_code == status.HTTP_200_OK:
            update_following(request.user, response)
            return Response(status=code.status_code)
        else:
            return Response({'error': response}, status=code.status_code)


class SpIsAuthenticated(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        is_authenticated = is_spotify_authenticated("AnonymousUser")
        return Response({'sp_is_auth': is_authenticated}, status=status.HTTP_200_OK)


class SpLogout(APIView):
    def get(self, request, format=None):
        remove_user_tokens("AnonymousUser")
        return Response({'sp_is_auth': is_spotify_authenticated("AnonymousUser")}, status=status.HTTP_200_OK)


class SpGetAuthURL(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        scopes = 'user-read-playback-state user-modify-playback-state user-read-currently-playing user-follow-read'

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
    return redirect("http://localhost:8080/")
