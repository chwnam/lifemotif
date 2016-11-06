from rest_framework import serializers

from emails.providers.gmail import models


class TidIndexSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TidIndex
        fields = '__all__'
        read_only = True


class MidIndexSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MidIndex
        fields = '__all__'
        read_only = True


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Profile
        fields = '__all__'
        read_only_fields = ('user', )
