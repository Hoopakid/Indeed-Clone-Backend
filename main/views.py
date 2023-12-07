from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import (
    RetrieveUpdateDestroyAPIView, GenericAPIView,
    RetrieveUpdateAPIView, ListAPIView
)
from rest_framework.decorators import permission_classes
from rest_framework import status

from django_elasticsearch_dsl_drf.filter_backends import (
    FilteringFilterBackend,
    SearchFilterBackend,
    SuggesterFilterBackend,
)

from elasticsearch_dsl import Q

from django_elasticsearch_dsl_drf.constants import SUGGESTER_COMPLETION
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
from django_elasticsearch_dsl_drf.pagination import PageNumberPagination

from .custom_filters import JobFilter, ResumeFilter
from .documents import DocumentJob
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
    ApplyJobSerializer, DocumentJobSerializer
)

from accounts.permissions import IsSuperUserPermission


class JobCreateAPIView(GenericAPIView):
    serializer_class = JobSerializer
    permission_classes = (CanCreateJobPermission,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class JobDetailAPIView(GenericAPIView):
    serializer_class = JobSerializer

    def get(self, request):
        queryset = UploadJob.objects.all()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status.HTTP_200_OK)


class JobUpdateAPIView(RetrieveUpdateAPIView):
    queryset = UploadJob.objects.all()
    serializer_class = JobSerializer
    permission_classes = (CanCreateJobPermission, IsHisObjectPermission)


class ResumeCreateAPIView(GenericAPIView):
    serializer_class = ResumeSerializer

    @permission_classes(IsAuthenticated)
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_200_OK)


class ResumeCreateWithFileAPIView(GenericAPIView):
    serializer_class = ResumeWithFileSerializer

    @permission_classes(IsAuthenticated)
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_200_OK)


class ResumeUpdateDestroyUpdateAPIView(RetrieveUpdateDestroyAPIView):
    queryset = CreateResumeOnIndeed.objects.all()
    serializer_class = ResumeSerializer
    permission_classes = (IsAuthenticated, IsHisObjectPermission)


class FileResumeDestroyAPIView(GenericAPIView):
    @permission_classes((IsHisObjectPermission, IsAuthenticated))
    def delete(self, request, pk):
        resume = get_object_or_404(UploadResumeWithFile, pk=pk)
        resume.delete()
        return Response(status.HTTP_204_NO_CONTENT)


class DestroyDiscountAPIView(GenericAPIView):
    @permission_classes((IsSuperUserPermission, IsHisObjectPermission))
    def delete(self, request, discount_id):
        discount = get_object_or_404(Discount, pk=discount_id)
        discount.delete()
        return Response(status.HTTP_204_NO_CONTENT)


class AddDiscountForPaymentAPIView(GenericAPIView):
    serializer_class = DiscountSerializer

    @permission_classes(IsSuperUserPermission)
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_200_OK)


class CreatePaymentOptionAPIView(GenericAPIView):
    serializer_class = PaymentSerializer

    def get(self, request):
        payment_option = PaymentOption.objects.all()
        serializer = self.get_serializer(payment_option, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    @permission_classes(IsSuperUserPermission)
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_200_OK)


class DestroyPaymentOptionAPIView(GenericAPIView):
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
            payment_option = get_object_or_404(PaymentOption, pk=int(payment_option_id))
            percentage_of_amount = payment_option.price * 100 / payment_option.discount.percentage_of_discount
            user_payment_card.payment_default_balance -= percentage_of_amount
            user_payment_card.save()

            # Creating of PaymentModel for the user
            payment_model = UserPaymentModel.objects.create(
                option=payment_option,
                payment_status=1,
                payed_amount=percentage_of_amount,
                user=request.user,
            )
            payment_model.save()
            return Response({'message': 'Payment successful'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApplyJobAPIView(GenericAPIView):
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


class GetAppliedJobs(GenericAPIView):
    serializer_class = ApplyJobSerializer

    def get(self, request):
        applied_jobs = ApplyJob.objects.filter(user=request.user)
        serializer = self.get_serializer(data=applied_jobs, many=True)
        return Response(serializer.data, status.HTTP_200_OK)


class ResumeFilterAPIView(ListAPIView):
    queryset = CreateResumeOnIndeed.objects.all()
    serializer_class = ResumeSerializer
    permission_classes = ()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ResumeFilter


class JobFilterAPIView(ListAPIView):
    queryset = UploadJob.objects.all()
    serializer_class = JobSerializer
    permission_classes = ()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = JobFilter


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class JobSearchViewSet(DocumentViewSet):
    document = DocumentJob
    serializer_class = DocumentJobSerializer
    pagination_class = CustomPageNumberPagination

    filter_backends = [
        FilteringFilterBackend,
        SearchFilterBackend,
        SuggesterFilterBackend,
    ]

    search_fields = (
        'company_name',
        'job_title',
        'experience',
    )

    filter_fields = {
        'company_name': 'company_name',
        'job_title': 'job_title',
        'experience': 'experience',
    }

    suggester_fields = {
        'company_name': {
            'field': 'company_name.suggest',
            'suggesters': [
                SUGGESTER_COMPLETION,
            ],
        },
        'job_title': {
            'field': 'job_title.suggest',
            'suggesters': [
                SUGGESTER_COMPLETION,
            ],
        },
        'experience': {
            'field': 'experience.suggest',
            'suggesters': [
                SUGGESTER_COMPLETION,
            ],
        }
    }

    def list(self, request, *args, **kwargs):
        search_term = self.request.query_params.get('search', '')
        query = Q('multi_match', query=search_term, fields=self.search_fields)
        queryset = self.filter_queryset(self.get_queryset().query(query))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
