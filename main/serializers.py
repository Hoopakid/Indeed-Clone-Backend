from django.contrib.auth.models import User
from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from rest_framework import serializers

from .models import UploadJob, CreateResumeOnIndeed, UploadResumeWithFile, Discount, PaymentOption, \
    UserPaymentCard, JobCreate, ApplyJob
from .documents import DocumentJob


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
        # read_only_fields = ('user',)


class ResumeWithFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadResumeWithFile
        fields = '__all__'
        read_only_fields = ('user',)


class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    discount = DiscountSerializer()

    class Meta:
        model = PaymentOption
        fields = '__all__'


class UserPaymentCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPaymentCard
        fields = ('card_number', 'expiry_date', 'security_code', 'user')


class JobCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobCreate
        fields = ('status', 'user')


class ApplyJobSerializer(serializers.ModelSerializer):
    job = JobSerializer()

    class Meta:
        model = ApplyJob
        fields = '__all__'
        read_only_fields = ('user',)


class DocumentJobSerializer(DocumentSerializer):
    class Meta:
        document = DocumentJob
        fields = ('company_name', 'job_title', 'experience')
