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


def update_following(current_user, following):
    for artist in following["artists"]["items"]:
        artist_obj = Artist.objects.filter(sp_id=artist["id"]).first()
        if artist_obj:
            artist_obj.following.add(current_user)
            artist_obj.save()
