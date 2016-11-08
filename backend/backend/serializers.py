from django_celery_results.models import TaskResult
from rest_framework import serializers

from . import models


class AsyncTaskResultSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.AsyncTaskResult
        fields = '__all__'
        read_only = True
