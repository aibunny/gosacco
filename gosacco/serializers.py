from django.contrib.auth.models import User
from rest_framework import serializers


class UserRegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'password', 'first_name', 'last_name', 'email')
