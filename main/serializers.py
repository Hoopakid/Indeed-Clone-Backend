from django.contrib.auth.models import User
from rest_framework import serializers

from main.models import UploadJob, CreateResumeOnIndeed, UploadResumeWithFile, Discount, PaymentOption, \
    UserPaymentCard, JobCreate, ApplyJob


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
        read_only_fields = ('user',)


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

