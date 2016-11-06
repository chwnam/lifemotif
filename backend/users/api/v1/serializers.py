from django.contrib.auth.models import User
from rest_framework import serializers

from emails.providers.gmail.serializers import ProfileSerializer


class UserSerializer(serializers.ModelSerializer):

    gmail_profiles = ProfileSerializer(many=True)

    class Meta:
        model = User
        exclude = ('password', )
        read_only_fields = ('emails', 'last_login', 'date_joined', )
