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
