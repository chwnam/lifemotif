from backend.app_settings.common.setting_helpers import get_env

LOGIN_REDIRECT_URL = '/'

AUTHENTICATION_BACKENDS = (
    # 'social.backends.google.GoogleOAuth2',
    'backend.social_auth_extension.backends.google.GoogleOauth2Extra',
    'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_URL_NAMESPACE = 'social'

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = get_env('GOOGLE_OAUTH2_CLIENT_ID', strict=True)
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = get_env('GOOGLE_OAUTH2_CLIENT_SECRET', strict=True)

SOCIAL_AUTH_GOOGLE_OAUTH2_AUTH_EXTRA_ARGUMENTS = {
    'access_type': 'offline',
    'approval_prompt': 'force',
}

SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
    'https://www.googleapis.com/auth/gmail.readonly',
]

SOCIAL_AUTH_GOOGLE_OAUTH2_EXTRA_DATA = [
    'updated_at',
]

SOCIAL_AUTH_USERNAME_IS_FULL_EMAIL = True
SOCIAL_AUTH_SLUGIFY_USERNAMES = False

SOCIAL_AUTH_PIPELINE = (
    # Get the information we can about the user and return it in a simple
    # format to create the user instance later. On some cases the details are
    # already part of the auth response from the provider, but sometimes this
    # could hit a provider API.
    'social.pipeline.social_auth.social_details',

    # Get the social uid from whichever service we're authing thru. The uid is
    # the unique identifier of the given user in the provider.
    'social.pipeline.social_auth.social_uid',

    # Verifies that the current auth process is valid within the current
    # project, this is where emails and domains whitelists are applied (if
    # defined).
    'social.pipeline.social_auth.auth_allowed',

    # Checks if the current social-account is already associated in the site.
    'social.pipeline.social_auth.social_user',

    # Make up a username for this person, appends a random string at the end if
    # there's any collision.
    'social.pipeline.user.get_username',

    # Send a validation email to the user to verify its email address.
    # Disabled by default.
    # 'social.pipeline.mail.mail_validation',

    # Associates the current social details with another user account with
    # a similar email address. Disabled by default.
    # 'social.pipeline.social_auth.associate_by_email',

    # Create a user account if we haven't found one yet.
    'social.pipeline.user.create_user',

    #################################################################################################################
    # /////////////////////////////|| //     // ////// ////// @@     @@   @@@@   @@@@@@ @@@@  @@@@@@
    # // LifeMotif Pipeline        || //     // //     //     @@@   @@@ @@    @@   @@    @@   @@
    # /////////////////////////////|| //     // ////// ////// @@ @@@ @@ @@    @@   @@    @@   @@@@@@
    # //                           || //     // //     //     @@ @@@ @@ @@    @@   @@    @@   @@
    # // Insert 'updated_at' field || //     // //     //     @@     @@ @@    @@   @@    @@   @@
    # /////////////////////////////|| ////// // //     ////// @@     @@   @@@@     @@   @@@@  @@
    #################################################################################################################
    'backend.social_auth_extension.pipeline.extra_fields.set_updated_at',

    # Create the record that associates the social account with the user.
    'social.pipeline.social_auth.associate_user',

    # Populate the extra_data field in the social record with the values
    # specified by settings (and the default ones like access_token, etc).
    'social.pipeline.social_auth.load_extra_data',

    # Update the user record with any changed info from the auth service.
    'social.pipeline.user.user_details',
)
