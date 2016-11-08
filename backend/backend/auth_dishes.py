from time import time
from datetime import datetime
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ImproperlyConfigured
from django.utils.module_loading import import_string
from social.apps.django_app.utils import load_strategy
from social.apps.django_app.default.models import UserSocialAuth


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


def get_auth_dish(auth_dish_path=None, **kwargs):
    """
    Auth dish factory class

    :param auth_dish_path: set None to get default dish class.
                           The default value is set by LIFEMOTIF_DEFAULT_AUTH_DISH in settings.py

    :param kwargs: arguments for passing a dish class.
                   if a dish class is PythonSocialAuthDish, then you are required to input at least 'user' instance.
                   e.g. get_auth_dish(user=request.user, request=request)
    :return:
    """
    if auth_dish_path:
        dotted_path = auth_dish_path
    else:
        dotted_path = settings.LIFEMOTIF_DEFAULT_AUTH_DISH

    if not dotted_path:
        raise ImproperlyConfigured('LIFEMOTIF_DEFAULT_AUTH_DISH setting not found!')

    arguments = {}

    if dotted_path == 'backend.auth_dishes.PythonSocialAuthDish':
        arguments['user'] = kwargs.get('user')
        arguments['request'] = kwargs.get('request')
        if 'provider' in kwargs:
            arguments['provider'] = kwargs['provider']
        # user keyword must be specified, and it must be an instance of User object
        if type(arguments['user']) is not User:
            raise TypeError(
                '\'PythonSocialAuthDish\' requires \'django.contrib.auth.models.User\' instance. '
                'Specify it by using \'user\' keyword.'
            )
    else:
        raise NotImplemented('\'{}\' is not a proper auth dish class'.format(dotted_path))

    auth_dish_class = import_string(dotted_path)

    if not issubclass(auth_dish_class, BaseAuthDish):
        raise TypeError(
            'auth_dish_class \'{}\' is not a subclass of BaseAuthDish'.format(
                type(auth_dish_class).__name__
            )
        )

    return auth_dish_class(**arguments)
