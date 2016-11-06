from social.backends.google import GoogleOAuth2
from time import time


# noinspection PyAbstractClass
class GoogleOauth2Extra(GoogleOAuth2):

    # Overloading of social.backends.oauth.BaseOAuth2.refresh_token
    def refresh_token(self, token, *args, **kwargs):

        response = super(GoogleOauth2Extra, self).refresh_token(token, *args, **kwargs)
        response['updated_at'] = int(time())

        return response
