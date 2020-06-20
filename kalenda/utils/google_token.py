import requests

from datetime import datetime, timezone, timedelta
from requests_oauthlib import OAuth2Session
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter

URL_BASE = 'https://oauth2.googleapis.com'


def check_google_token(token):
    endpoint = f'/tokeninfo?id_token={token}'
    print(token)
    url = URL_BASE + endpoint
    r = requests.get(url)
    print(r.json())
    if r.status_code == 200:
        return True
    return False


def _get_oauth2_session_client(social_account):
    refresh_token_url = GoogleOAuth2Adapter.access_token_url
    social_token = social_account.socialtoken_set.first()

    def _token_updater(new_token):
        social_token.token = new_token['access_token']
        social_token.token_secret = new_token['refresh_token']
        social_token.expires_at = (
            datetime.now(timezone.utc) +
            timedelta(seconds=int(new_token['expires_in']))
        )
        social_token.save()

    client_id = social_token.app.client_id
    client_secret = social_token.app.secret

    extra = {
        'client_id': client_id,
        'client_secret': client_secret,
    }

    expires_in = (
        social_token.expires_at - datetime.now(timezone.utc)
    ).total_seconds()
    token = {
        'access_token': social_token.token,
        'refresh_token': social_token.token_secret,
        'token_type': 'Bearer',
        'expires_in': expires_in
    }

    client = OAuth2Session(
        client_id, token=token, auto_refresh_url=refresh_token_url,
        auto_refresh_kwargs=extra, token_updater=_token_updater
    )

    return client


def check_google_account(social_account):
    client = _get_oauth2_session_client(social_account)
    resp = client.get(GoogleOAuth2Adapter.profile_url)
    extra_data = resp.json()
    new_email = extra_data['email']
    return social_account


