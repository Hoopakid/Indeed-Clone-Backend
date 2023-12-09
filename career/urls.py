from django.urls import path

from career.views import (
    GetResumesOrJobsAPIView, CreateSalaryAPIView,
    IndustryAPIView, ChatListCreateAPIView,
    MessageListCreateAPIView, ReplyMessageAPIVIew,
    DestroyIndustryAPIView
)

urlpatterns = [
    # get the section for your role (employer or seeker)
    path('get-resume-or-job', GetResumesOrJobsAPIView.as_view(), name='get-resume-or-job'),
    # CRUD of admin role
    path('create-salary', CreateSalaryAPIView.as_view(), name='create-salary'),
    path('create-industry', IndustryAPIView.as_view(), name='create-industry'),
    path('destroy-industry', DestroyIndustryAPIView.as_view(), name='create-industry'),

    # chat with other people or admin and you can do reply messages
    path('create-chat-list', ChatListCreateAPIView.as_view(), name='create-chat-list'),
    path('create-message-list', MessageListCreateAPIView.as_view(), name='create-message-list'),
    path('reply-message/<int:message_id>', ReplyMessageAPIVIew.as_view(), name='reply-message'),
]
