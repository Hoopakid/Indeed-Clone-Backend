from django.shortcuts import get_object_or_404

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import (
    RetrieveUpdateDestroyAPIView, GenericAPIView,
    RetrieveUpdateAPIView
)
from rest_framework.views import APIView
from rest_framework.decorators import permission_classes
from rest_framework import status

from .models import (
    UploadJob, UploadResumeWithFile,
    CreateResumeOnIndeed, Discount,
    PaymentOption, UserPaymentCard,
    JobCreate, UserPaymentModel,
    ApplyJob
)
from .permission import CanCreateJobPermission, IsHisObjectPermission
from .serializers import (
    JobSerializer, ResumeSerializer,
    ResumeWithFileSerializer, DiscountSerializer,
    PaymentSerializer, UserPaymentCardSerializer,
    ApplyJobSerializer
)

from accounts.permissions import IsSuperUserPermission


class JobCreateAPIView(APIView):
    @permission_classes(CanCreateJobPermission)
    def post(self, request, *args, **kwargs):
        serializer = JobSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class JobDetailAPIView(APIView):
    def get(self, request):
        queryset = UploadJob.objects.all()
        serializer = JobSerializer(queryset, many=True)
        return Response(serializer.data, status.HTTP_200_OK)


class JobUpdateAPIView(RetrieveUpdateAPIView):
    queryset = UploadJob.objects.all()
    serializer_class = JobSerializer
    permission_classes = (CanCreateJobPermission, IsHisObjectPermission)


class ResumeCreateAPIView(APIView):
    @permission_classes(IsAuthenticated)
    def post(self, request, *args, **kwargs):
        serializer = ResumeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_200_OK)


class ResumeCreateWithFileAPIView(APIView):
    @permission_classes(IsAuthenticated)
    def post(self, request, *args, **kwargs):
        serializer = ResumeWithFileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_200_OK)


class ResumeUpdateDestroyUpdateAPIView(RetrieveUpdateDestroyAPIView):
    queryset = CreateResumeOnIndeed.objects.all()
    serializer_class = ResumeSerializer
    permission_classes = (IsAuthenticated, IsHisObjectPermission)


class FileResumeDestroyAPIView(APIView):
    @permission_classes((IsHisObjectPermission, IsAuthenticated))
    def delete(self, request, pk):
        resume = get_object_or_404(UploadResumeWithFile, pk=pk)
        resume.delete()
        return Response(status.HTTP_204_NO_CONTENT)


class DestroyDiscountAPIView(APIView):
    @permission_classes((IsSuperUserPermission, IsHisObjectPermission))
    def delete(self, request, discount_id):
        discount = get_object_or_404(Discount, pk=discount_id)
        discount.delete()
        return Response(status.HTTP_204_NO_CONTENT)


class AddDiscountForPaymentAPIView(APIView):
    @permission_classes(IsSuperUserPermission)
    def post(self, request):
        serializer = DiscountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_200_OK)


class CreatePaymentOptionAPIView(APIView):
    def get(self, request):
        payment_option = PaymentOption.objects.all()
        serializer = PaymentSerializer(payment_option, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    @permission_classes(IsSuperUserPermission)
    def post(self, request):
        serializer = PaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_200_OK)


class DestroyPaymentOptionAPIView(APIView):
    @permission_classes((IsSuperUserPermission, IsHisObjectPermission))
    def delete(self, request, payment_id):
        payment_option = get_object_or_404(PaymentOption, pk=payment_id)
        payment_option.delete()
        return Response(status.HTTP_204_NO_CONTENT)


class ProcessPaymentAPIView(GenericAPIView):
    serializer_class = UserPaymentCardSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, payment_option_id):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user_payment_card = get_object_or_404(
                UserPaymentCard,
                card_number=serializer.validated_data['card_number'],
                expiry_date=serializer.validated_data['expiry_date'],
                security_code=serializer.validated_data['security_code']
            )
            user = user_payment_card.user
            # Set the status of the user to Yes
            job_create = get_object_or_404(JobCreate, user=user)
            job_create.status = JobCreate.YES
            job_create.save()

            # Subtract the payment balance from the user's balance
            payment_option = get_object_or_404(PaymentOption, pk=payment_option_id)
            percentage_of_amount = payment_option.price * 100 / payment_option.discount.percentage_of_discount
            user_payment_card.payment_default_balance -= percentage_of_amount
            user_payment_card.save()

            # Creating of the PaymentModel for the user
            payment_model = UserPaymentModel.objects.create(
                option=payment_option.id,
                payment_status="Payment Successful",
                payed_amount=percentage_of_amount,
                user=request.user,
            )
            payment_model.save()
            return Response({'message': 'Payment successful'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApplyJobAPIView(APIView):
    @permission_classes(IsAuthenticated)
    def post(self, request, job_id):
        if UploadJob.objects.filter(pk=job_id).exists():
            serializer = ApplyJobSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status.HTTP_200_OK)
        return Response(status.HTTP_404_NOT_FOUND)

    @permission_classes((IsAuthenticated, IsHisObjectPermission))
    def delete(self, request, job_id):
        job = get_object_or_404(ApplyJob, pk=job_id)
        job.delete()
        return Response(status.HTTP_204_NO_CONTENT)


class GetAppliedJobs(APIView):
    def get(self, request):
        applied_jobs = ApplyJob.objects.filter(user=request.user)
        serializer = ApplyJobSerializer(data=applied_jobs, many=True)
        return Response(serializer.data, status.HTTP_200_OK)
