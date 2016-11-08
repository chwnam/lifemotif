from django.contrib.auth.models import User
from django.db import models
from django_celery_results.models import TaskResult

job_type_choices = (
    ('gmail-update', 'emails.tasks.update_gmail_message_index'),
)


class AsyncTaskResult(models.Model):

    task_id = models.CharField(unique=True, max_length=40)

    user = models.ForeignKey(User)

    created = models.DateTimeField(auto_now_add=True)

    job_type = models.CharField(choices=job_type_choices, max_length=20)
