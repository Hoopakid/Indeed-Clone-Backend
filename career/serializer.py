from rest_framework import serializers

from accounts.models import UserContactInformation
from career.models import SalaryByIndustry, Industry, Message, Chat
from main.models import CreateResumeOnIndeed, UploadJob
from main.serializers import ResumeSerializer, JobSerializer


class SalarySerializer(serializers.ModelSerializer):
    class Meta:
        model = SalaryByIndustry
        fields = '__all__'
        read_only_fields = ('slug',)


class IndustrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Industry
        fields = '__all__'


class UserContactInformationSerializer(serializers.ModelSerializer):
    resumes = ResumeSerializer(many=True, read_only=True)
    jobs = JobSerializer(many=True, read_only=True)

    class Meta:
        model = UserContactInformation
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        whoami = data.get('whoami')
        if whoami == UserContactInformation.EmployerOrSeeker.EMPLOYER:
            resume_data = CreateResumeOnIndeed.objects.filter(user=instance.user)
            data['resume'] = ResumeSerializer(resume_data, many=True).data
        elif whoami == UserContactInformation.EmployerOrSeeker.SEEKER:
            job_data = UploadJob.objects.filter(user=instance.user)
            data['jobs'] = JobSerializer(job_data, many=True).data

        return data


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = '__all__'
