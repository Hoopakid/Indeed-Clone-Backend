from rest_framework import serializers
from django.contrib.auth.models import User

from accounts.models import CreateResumeOnIndeed


# from accounts.models import CreateResumeOnIndeed


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreateResumeOnIndeed
        fields = '__all__'


class UserRegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(max_length=255, write_only=True)
    password2 = serializers.CharField(max_length=255, write_only=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
