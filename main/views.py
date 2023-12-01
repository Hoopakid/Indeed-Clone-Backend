from django.contrib.auth.models import User
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics, status

from main.models import JobCreate, UploadJob, UploadResumeWithFile, CreateResumeOnIndeed
from main.permission import CanCreateJobPermission
from main.serializers import UserSerializer, JobSerializer, ResumeSerializer, ResumeWithFileSerializer


class JobCreateAPIView(generics.GenericAPIView):
    queryset = UploadJob.objects.all()
    serializer_class = JobSerializer
    permission_classes = CanCreateJobPermission

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class JobDetailAPIView(generics.GenericAPIView):
    queryset = UploadJob.objects.all()
    serializer_class = JobSerializer
    permission_classes = ()

    def get(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class JobUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = UploadJob.objects.all()
    serializer_class = JobSerializer
    permission_classes = (CanCreateJobPermission,)


class ResumeCreateAPIView(generics.GenericAPIView):
    queryset = CreateResumeOnIndeed.objects.all()
    serializer_class = ResumeSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ResumeCreateWithFileAPIView(generics.GenericAPIView):
    queryset = UploadResumeWithFile.objects.all()
    serializer_class = ResumeWithFileSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ResumeUpdateDestroyUpdateAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CreateResumeOnIndeed
    serializer_class = ResumeSerializer
    permission_classes = (IsAuthenticated,)


class FileResumeDestroyAPIView(generics.GenericAPIView):
    queryset = UploadResumeWithFile.objects.all()
    serializer_class = ResumeWithFileSerializer

    def delete(self, request, pk):
        resume_instance = get_object_or_404(UploadResumeWithFile, pk=pk)
        resume_instance.delete()
        return Response({"success": True, "status": status.HTTP_204_NO_CONTENT})
