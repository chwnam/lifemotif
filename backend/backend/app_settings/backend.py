import os

from backend.app_settings.common.path_settings import PROJECT_DIR

LIFEMOTIF_DEFAULT_STATICFILES_DIR = os.path.join(PROJECT_DIR, 'staticfiles')

LIFEMOTIF_DEFAULT_AUTH_DISH = 'backend.auth_dishes.PythonSocialAuthDish'
