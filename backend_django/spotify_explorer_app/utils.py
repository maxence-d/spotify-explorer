from datetime import timedelta

from django.utils import timezone

from requests import post, put, get

from .credentials import CLIENT_ID, CLIENT_SECRET
from .models import SpotifyToken

BASE_URL = "https://api.spotify.com/v1/"


def get_user_tokens(session_id):
    return SpotifyToken.objects.filter(user=session_id).first()


def get_or_make_user_token(session_id, access_token, token_type, expires_in, refresh_token):
    tokens = get_user_tokens(session_id)
    expires_in = timezone.now() + timedelta(seconds=expires_in)

    if tokens:
        tokens.access_token = access_token
        tokens.refresh_token = refresh_token
        tokens.expires_in = expires_in
        tokens.token_type = token_type
        tokens.save(update_fields=['access_token',
                                   'refresh_token', 'expires_in', 'token_type'])
    else:
        tokens = SpotifyToken(user="AnonymousUser", access_token=access_token,
                              refresh_token=refresh_token, token_type=token_type, expires_in=expires_in)
        tokens.save()


def refresh_spotify_token(session_id):
    refresh_token = get_user_tokens(session_id).refresh_token

    response = post('https://accounts.spotify.com/api/token', data={
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }).json()

    access_token = response.get('access_token')
    token_type = response.get('token_type')
    expires_in = response.get('expires_in')

    get_or_make_user_token(access_token, token_type, expires_in, refresh_token)


def is_spotify_authenticated(session_id):
    sp_token = get_user_tokens(session_id)
    if sp_token:
        expiry = sp_token.expires_in
        if expiry <= timezone.now():
            refresh_spotify_token(session_id)
        return True
    return False


def execute_spotify_api_request(endpoint=None, session_id="AnonymousUser", post_=False, put_=False):
    tokens = get_user_tokens(session_id)
    headers = {'Content-Type': 'application/json',
               'Authorization': "Bearer " + tokens.access_token}
    if post_:
        post(BASE_URL + endpoint, headers=headers)
    if put_:
        put(BASE_URL + endpoint, headers=headers)

    print(BASE_URL + endpoint)
    response = get(BASE_URL + endpoint, {}, headers=headers)
    try:
        return response.json()
    except:
        return {'Error': 'Issue with request'}
