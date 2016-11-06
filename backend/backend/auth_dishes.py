from time import time
from datetime import datetime

from social.apps.django_app.default.models import UserSocialAuth
from social.apps.django_app.utils import load_strategy


class BaseAuthDish(object):

    expiration_margin = 300  # 5 minutes

    @staticmethod
    def now():
        return int(time())

    @property
    def user_email(self):
        raise NotImplemented('Not implemented!')

    @property
    def access_token(self):
        raise NotImplemented('Not implemented!')

    @property
    def refresh_token(self):
        raise NotImplemented('Not implemented!')

    @property
    def expires_in(self):
        raise NotImplemented('Not implemented!')

    @property
    def updated_at(self):
        raise NotImplemented('Not implemented!')

    @property
    def default_request_header(self):
        raise NotImplemented('Not implemented!')

    def do_refresh(self):
        """
        Refresh access token
        :return:
        """
        raise NotImplemented('Not implemented!')

    def get_request_func(self):
        """
        Return request(url, *args, **kwargs) function
        :return:
        """
        raise NotImplemented('Not implemented!')

    # End of unimplemented methods ###########

    @property
    def expiration_datetime(self):
        return datetime.utcfromtimestamp(self.updated_at + self.expires_in)

    @property
    def expiration_left(self):
        return self.now() - self.updated_at

    @property
    def is_expired(self):
        return self.now() >= self.updated_at + self.expires_in

    @property
    def is_time_to_refresh(self):
        return self.now() >= self.updated_at + self.expires_in - self.expiration_margin


class PythonSocialAuthDish(BaseAuthDish):

    def __init__(self, user, request=None, provider='google-oauth2'):
        self.user = user
        self.request = request
        self.provider = provider

        self.strategy = load_strategy(request)
        self.user_social = UserSocialAuth.get_social_auth_for_user(user=self.user, provider=self.provider)[0]
        self.backend = self.user_social.get_backend_instance(strategy=self.strategy)

    @property
    def user_email(self):
        return self.user_social.uid

    @property
    def access_token(self):
        if self.is_time_to_refresh:
            self.do_refresh()
        return self.user_social.extra_data.get('access_token')

    @property
    def refresh_token(self):
        return self.user_social.extra_data.get('refresh_token')

    @property
    def expires_in(self):
        return self.user_social.extra_data.get('expires')

    @property
    def updated_at(self):
        """
        An extra data created by our project. See backend.social_auth_extension
        :return:
        """
        return self.user_social.extra_data.get('updated_at')

    @property
    def default_request_header(self):
        return {
            'Authorization': 'Bearer %s' % self.access_token,
            'Accept-Encoding': 'gzip',
        }

    def do_refresh(self):
        self.user_social.refresh_token(self.strategy)

    def get_request_func(self):
        return self.backend.get_json
