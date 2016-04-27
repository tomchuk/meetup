import requests
from django.conf import settings

from .models import User

TOKEN_URL = 'https://graph.facebook.com/debug_token'
FB_ME_URL = 'https://graph.facebook.com/v2.6/me'
FB_FIELDS = 'id,email,first_name,last_name'

NO_TOKEN = 'no token'
INVALID_TOKEN = 'invalid token'
BAD_RESPONSE = 'bad response'
MISSING_ID = 'missing id'


class TokenException(Exception):
    pass


class FacebookBackend(object):

    def _check_token(self, token):
        if not token:
            raise TokenException(NO_TOKEN)

        token_debug = requests.get(
          TOKEN_URL,
          params={
            'input_token': token,
            'access_token': '{}|{}'.format(
              settings.FB_APP_ID,
              settings.FB_APP_SECRET
            )
          }
        )

        if token_debug.status_code != 200:
            raise TokenException(BAD_RESPONSE)
        if not token_debug.json().get('data', {}).get('is_valid', False):
            raise TokenException(INVALID_TOKEN)

    def _fetch_user_data(self, token):
        user_data = requests.get(
          FB_ME_URL,
          params={
            'access_token': token,
            'fields': FB_FIELDS,
          }
        )
        if user_data.status_code != 200:
            raise TokenException(BAD_RESPONSE)

        user_data = user_data.json()

        if 'id' not in user_data or not user_data['id']:
            raise TokenException(MISSING_ID)
        return user_data

    def authenticate(self, token=None):

        try:
            self._check_token(token)
            user_data = self._fetch_user_data(token)
        except TokenException:
            return None

        user, created = User.objects.get_or_create(id=user_data['id'])
        user.access_token = token
        user.first_name = user_data.get('first_name', user.first_name)
        user.last_name = user_data.get('last_name', user.last_name)
        user.email = user_data.get('email', user.email)
        user.save()
        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None
