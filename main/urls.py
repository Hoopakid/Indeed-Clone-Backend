from django.urls import path, include

from main.views import JobCreateAPIView, JobDetailAPIView, JobUpdateAPIView, ResumeCreateAPIView, \
    ResumeCreateWithFileAPIView, ResumeUpdateDestroyUpdateAPIView, FileResumeDestroyAPIView, \
    AddDiscountForPaymentAPIView, DestroyDiscountAPIView, CreatePaymentOptionAPIView, DestroyPaymentOptionAPIView, \
    ProcessPaymentAPIView, ApplyJobAPIView, GetAppliedJobs, ResumeFilterAPIView, JobFilterAPIView, JobSearchViewSet

from rest_framework import routers

router = routers.DefaultRouter(trailing_slash=False)
router.register('job-search', JobSearchViewSet, basename='search_job')

urlpatterns = [
    # CRUD API of jobs
    path('upload-job', JobCreateAPIView.as_view(), name='upload-job'),
    path('job-detail', JobDetailAPIView.as_view(), name='detail-job'),
    path('job-update/<int:product_id>', JobUpdateAPIView.as_view(), name='job-update'),

    # CRUD API of resume and resume with file
    path('resume-create', ResumeCreateAPIView.as_view(), name='resume-create'),
    path('resume-create-with-file', ResumeCreateWithFileAPIView.as_view(), name='resume-create-with-file'),
    path('resume-update/<int:product_id>', ResumeUpdateDestroyUpdateAPIView.as_view(), name='resume-update'),
    path('file-resume-delete/<int:product_id>', FileResumeDestroyAPIView.as_view(), name='file-resume-update'),

    # CD Discount for Payment API
    path('create-discount', AddDiscountForPaymentAPIView.as_view(), name='create-discount'),
    path('delete-discount/<int:discount_id>', DestroyDiscountAPIView.as_view(), name='destroy-discount'),
    path('create-payment-option', CreatePaymentOptionAPIView.as_view(), name='create-payment-option'),
    path('delete-payment-option/<int:payment_id>', DestroyPaymentOptionAPIView.as_view(), name='create-payment-option'),

    # processing of the user's payment for creating job
    path('process-payment/<int:payment_option_id>', ProcessPaymentAPIView.as_view(), name='process-payment'),

    # CRD for apply jobs
    path('apply-job/<int:job_id>', ApplyJobAPIView.as_view(), name='apply-job'),
    path('get-applied-jobs', GetAppliedJobs.as_view(), name='get-applied-jobs'),

    # filters for resume and job
    path('resume-filter', ResumeFilterAPIView.as_view(), name='resume-filter'),
    path('job-filter', JobFilterAPIView.as_view(), name='job-filter'),

    # including search set
    path('', include(router.urls)),
]
