"""
Gmail API v1 Views
"""
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope, TokenHasScope
from rest_framework import (generics, permissions, )
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED

from backend.auth_dishes import get_auth_dish
from backend.models import AsyncTaskResult
from backend.serializers import AsyncTaskResultSerializer
from emails.tasks import update_gmail_message_index
from emails.providers.gmail import (models, serializers, )
from emails.providers.gmail.api import GmailApi


################################################################################
# TID Index Views
################################################################################
class TidIndexView(generics.ListAPIView):
    queryset = models.TidIndex.objects.all()
    serializer_class = serializers.TidIndexSerializer


class TidIndexDetailView(generics.RetrieveAPIView):
    queryset = models.TidIndex.objects.all()
    serializer_class = serializers.TidIndexSerializer


################################################################################
# MID Index Views
################################################################################
class MidIndexView(generics.ListAPIView):
    queryset = models.MidIndex.objects.all()
    serializer_class = serializers.MidIndexSerializer


class MidIndexDetailView(generics.RetrieveAPIView):
    queryset = models.MidIndex.objects.all()
    serializer_class = serializers.MidIndexSerializer


################################################################################
# Gmail Profile Index Views
################################################################################
class ProfilesView(generics.ListCreateAPIView):
    queryset = models.Profile.objects.all()
    serializer_class = serializers.ProfileSerializer

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.validated_data.update({'user_id': self.request.user.id})
            super(ProfilesView, self).perform_create(serializer)


class ProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Profile.objects.all()
    serializer_class = serializers.ProfileSerializer


class LabelsView(APIView):
    """
    A kind of Gmail's 'list label' API proxy
    """
    _ignore_model_permissions = True

    def _allowed_methods(self):
        return ['GET']

    @staticmethod
    def get(request, *args, **kwargs):
        auth_dish = get_auth_dish(user=request.user, request=request)
        api = GmailApi(auth_dish=auth_dish)
        labels = api.get_labels()
        return Response(labels)


class UpdateIndexView(APIView):

    _ignore_model_permissions = True

    def _allowed_methods(self):
        return ['POST']

    @staticmethod
    def post(request, *args, **kwargs):

        if settings.LIFEMOTIF_TASK_TYPE == 'celery':
            async_result = update_gmail_message_index.delay(request.user.id)
            task_result = AsyncTaskResult.objects.create(
                task_id=async_result.task_id,
                user=request.user,
                job_type='gmail-update'
            )
            serializer = AsyncTaskResultSerializer(instance=task_result)

            return Response(data=serializer.data, status=HTTP_201_CREATED)

        elif settings.LIFEMOTIF_TASK_TYPE == 'direct':
            update_gmail_message_index(request.user.id)
            return Response(data={}, status=HTTP_201_CREATED)

        else:
            raise ImproperlyConfigured(
                'You must declare LIFEMOTIF_TASK_TYPE in the settings, and set the value as \'celery\', or \'direct\''
            )
