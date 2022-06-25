import json
from pprint import pprint

from .models import Artist


def get_or_make_artist_from_sp(sp_id, sp_artist=None):
    pprint(sp_artist)
    artist = Artist.objects.filter(sp_id=sp_id).first()
    if not artist:
        artist = Artist(sp_id=sp_artist["id"],
                        name=sp_artist["name"],
                        followers=sp_artist["followers"]["total"],
                        image_url=sp_artist["images"][0]["url"]
                        )
        artist.save()
    return artist
#  if tokens:
#      tokens.access_token = access_token
#      tokens.refresh_token = refresh_token
#      tokens.expires_in = expires_in
#      tokens.token_type = token_type
#      tokens.save(update_fields=['access_token',
#                                 'refresh_token', 'expires_in', 'token_type'])
#  else:
#      tokens = SpotifyToken(user="AnonymousUser", access_token=access_token,
#                            refresh_token=refresh_token, token_type=token_type, expires_in=expires_in)
#      tokens.save()
