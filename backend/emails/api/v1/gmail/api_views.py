"""
Gmail API v1 Views
"""
from rest_framework import (
    generics,
    permissions
)
from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope, TokenHasScope
from rest_framework.exceptions import NotAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from backend.auth_dishes import PythonSocialAuthDish
from emails.providers.gmail import (
    models,
    serializers,
)
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
        auth_dish = PythonSocialAuthDish(user=request.user, request=request, provider='google-oauth2')
        api = GmailApi(auth_dish=auth_dish)
        labels = api.get_labels()
        return Response(labels)


class UpdateIndexView(APIView):
    _ignore_model_permissions = True

    def _allowed_methods(self):
        return ['POST']

    @staticmethod
    def post(request, *args, **kwargs):
        pass
