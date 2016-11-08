from django.contrib.auth.models import User

from backend import celery_app
from backend.auth_dishes import get_auth_dish

from emails.providers.gmail.api import GmailApi
from emails.providers.gmail.models import Profile
from emails.providers.gmail.services import IndexService


@celery_app.task
def update_gmail_message_index(user_id):

    user = User.objects.get(id=user_id)
    profile = Profile.objects.get(user=user)
    auth_dish = get_auth_dish(user=user, request=None)

    return IndexService(gmail_api=GmailApi(auth_dish=auth_dish), profile=profile).update_index()


@celery_app.task
def test_task(x, y):
    return x + y
