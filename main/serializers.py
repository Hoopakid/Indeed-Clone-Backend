from django.contrib.auth.models import User
from rest_framework import serializers

from main.models import UploadJob, CreateResumeOnIndeed, UploadResumeWithFile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadJob
        fields = '__all__'


class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreateResumeOnIndeed
        fields = '__all__'


class ResumeWithFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadResumeWithFile
        fields = '__all__'
