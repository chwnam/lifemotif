LOGIN_REDIRECT_URL = '/'

AUTHENTICATION_BACKENDS = (
    'social.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_URL_NAMESPACE = 'social'

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '557620163613-bgan3ptoeols4scjscti1ktnah67udsb.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'YqwOJFDATr2oJOlN-o6Da87s'

# SOCIAL_AUTH_GOOGLE_OAUTH2_AUTH_EXTRA_ARGUMENTS = {
#       'access_type': 'offline'
# }

SOCIAL_AUTH_USERNAME_IS_FULL_EMAIL = True
SOCIAL_AUTH_SLUGIFY_USERNAMES = False
