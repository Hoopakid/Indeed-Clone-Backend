from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics

from main.serializers import UserSerializer


# Create your views here.

# class JobCreateApiView(generics.GenericAPIView):
#     permission_classes =
#     pass
