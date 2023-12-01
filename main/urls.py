from django.urls import path

from main.views import JobCreateAPIView, JobDetailAPIView, JobUpdateAPIView, ResumeCreateAPIView, \
    ResumeCreateWithFileAPIView, ResumeUpdateDestroyUpdateAPIView, FileResumeDestroyAPIView

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
]
