from time import time
from unittest.mock import patch, ANY

from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory
from social.apps.django_app.default.models import UserSocialAuth
from social.apps.django_app.utils import load_strategy

from backend.social_auth_extension.backends.google import GoogleOauth2Extra
from emails.api.v1.gmail import (
    get_user_social, get_user_social_and_backend_instance, refresh_user_token_if_token_about_to_expire
)


class DiemGoogleFactoryTestCase(TestCase):

    user = None
    user_social = None
    factory = RequestFactory()

    def setUp(self):
        self.user = User.objects.create_user(
            username='google-factory-test',
            email='google-factory-test@lifemotif.changwoo.pe.kr',
            password='google-factory-test-password'
        )
        self.user.save()

        self.user_social = UserSocialAuth.objects.create(
            user=self.user,
            provider='google-oauth2',
            uid=self.user.email,
        )
        self.user_social.save()

    def test_get_user_social(self):
        """
        test get_user_social() function
        :return:
        """
        request = self.factory.get('/')
        request.user = self.user
        request.session = {}

        user_social = get_user_social(request)

        self.assertEqual(self.user_social, user_social, 'self.user_social != user_social')

    def test_get_user_social_and_backend_instance(self):
        """
        test get_social_and_backend_instance() function
        :return:
        """
        request = self.factory.get('/')
        request.user = self.user
        request.session = {}

        user_social, backend = get_user_social_and_backend_instance(request)

        self.assertEqual(self.user_social, user_social, 'self.user_social != user_social')
        self.assertIsInstance(backend, GoogleOauth2Extra, 'backend is not an instance of GoogleOauth2Extra')

    @patch('social.apps.django_app.default.models.UserSocialAuth.refresh_token')
    def test_refresh_user_token_if_token_about_to_expire(self, mock_refresh_token):
        """
        test refresh_user_token_if_token_about_to_expire() function
        :return:
        """
        expires_in = 3600
        margin = 300

        request = self.factory.get('/')
        request.user = self.user
        request.session = {}

        user_social = get_user_social(request)
        strategy = load_strategy(request)

        # assume the token is expired, so refresh_token() will be called
        user_social.extra_data['updated_at'] = int(time() - (expires_in + margin + 10))
        user_social.extra_data['expires_in'] = expires_in
        user_social.save()

        refresh_user_token_if_token_about_to_expire(user_social, strategy)
        mock_refresh_token.assert_called_with(ANY)

        # now the token is not expired.
        mock_refresh_token.reset_mock()
        user_social.extra_data['updated_at'] = int(time() - margin)
        user_social.extra_data['expires_in'] = expires_in
        user_social.save()

        refresh_user_token_if_token_about_to_expire(user_social, strategy)
        mock_refresh_token.assert_not_called()
