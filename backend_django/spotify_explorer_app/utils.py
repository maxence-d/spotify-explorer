
from django.utils import timezone

def is_spotify_authenticated(sp_token):
    if sp_token:
        expiry = sp_token.expires_in
        if expiry <= timezone.now():
            pass
            # refresh_spotify_token(session_id)
        return True
    return False

