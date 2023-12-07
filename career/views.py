from django.shortcuts import get_object_or_404
from rest_framework import status, decorators
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from accounts.models import UserContactInformation
from accounts.permissions import IsSuperUserPermission
from .models import Message, Chat, Industry
from .permissons import IsAdminOrParticipant

from .serializer import (
    UserContactInformationSerializer,
    SalarySerializer, IndustrySerializer,
    MessageSerializer, ChatSerializer
)


class GetResumesOrJobsAPIView(GenericAPIView):
    serializer_class = UserContactInformationSerializer

    def get(self, request):
        user_info = UserContactInformation.objects.all()
        serializer = self.get_serializer(user_info, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateSalaryAPIView(GenericAPIView):
    serializer_class = SalarySerializer

    @decorators.permission_classes(IsSuperUserPermission)
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class IndustryAPIView(GenericAPIView):
    serializer_class = IndustrySerializer

    @decorators.permission_classes(IsSuperUserPermission)
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class DestroyIndustryAPIView(GenericAPIView):
    @decorators.permission_classes(IsSuperUserPermission)
    def delete(self, request, industry_id):
        industry = get_object_or_404(Industry, pk=industry_id)
        industry.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ChatListCreateAPIView(GenericAPIView):
    permission_classes = (IsAdminOrParticipant,)
    serializer_class = ChatSerializer

    def get(self, request):
        chats = Chat.objects.all()
        serializer = self.get_serializer(chats, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MessageListCreateAPIView(GenericAPIView):
    serializer_class = MessageSerializer
    permission_classes = (IsAdminOrParticipant,)

    def get(self, request):
        chats = Message.objects.all()
        serializer = self.get_serializer(chats, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReplyMessageAPIVIew(GenericAPIView):
    @decorators.permission_classes(IsAdminOrParticipant)
    def put(self, request, message_id):
        message = get_object_or_404(Message, pk=message_id)
        serializer = MessageSerializer(message, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
