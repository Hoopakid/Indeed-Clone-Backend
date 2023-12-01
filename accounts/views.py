import os

import requests
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from rest_framework import generics, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view

from allauth.socialaccount.models import SocialApp
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView

from .models import UserContactInformation
from .serializers import UserSerializer, UserRegisterSerializer, LogoutSerializer, ContactSerializer

User = get_user_model()


class RegisterAPIView(GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]
    serializer_class = UserRegisterSerializer

    def post(self, request):
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        username = request.POST.get('username')

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                return Response({'success': False, 'error': 'This username already exists.'}, status=400)
            if User.objects.filter(email=email).exists():
                return Response({'success': False, 'error': 'This email already exists.'}, status=400)
            user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=username,
                password=password1,
                email=email
            )
            user_serializer = UserSerializer(user)
            return Response({'success': True, 'data': user_serializer.data})
        else:
            return Response({'success': False, 'message': 'Passwords are not same!'},
                            status=status.HTTP_400_BAD_REQUEST)


class LogoutAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = LogoutSerializer

    def post(self, request):
        refresh_token = request.data.get('refresh')
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response(status=204)


class UserInfoAPIView(GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        user_serializer = self.get_serializer(data=user)
        return Response(user_serializer.data)


class RedirectToGoogleAPIView(GenericAPIView):

    def get(self, request):
        google_redirect_uri = os.getenv('GOOGLE_REDIRECT_URI')
        try:
            google_client_id = SocialApp.objects.get(provider='google').client_id
        except SocialApp.DoesNotExist:
            return Response({'success': False, 'message': 'SocialApp does not exist'}, status=404)
        url = f'https://accounts.google.com/o/oauth2/v2/auth?redirect_uri={google_redirect_uri}&prompt=consent&response_type=code&client_id={google_client_id}&scope=openid email profile&access_type=offline'
        return redirect(url)


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = 'https://75f8-185-139-138-214.ngrok-free.app/accounts/google/callback'
    client_class = OAuth2Client


class GithubLogin(SocialLoginView):
    adapter_class = GitHubOAuth2Adapter
    callback_url = 'https://75f8-185-139-138-214.ngrok-free.app/accounts/github/callback'
    client_class = OAuth2Client


@api_view(["GET"])
def callback(request):
    code = request.GET.get("code")
    res = requests.post("http://localhost:8000/accounts/google", data={"code": code}, timeout=30)
    return Response(res.json())


@api_view(["GET"])
def callback_github(request):
    code = request.GET.get("code")
    res = requests.post("http://localhost:8000/accounts/github", data={"code": code}, timeout=30)
    return Response(res.json())


class ContactCreateAPIView(generics.GenericAPIView):
    queryset = UserContactInformation.objects.all()
    serializer_class = ContactSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ContactUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserContactInformation.objects.all()
    serializer_class = ContactSerializer
    permission_classes = (IsAuthenticated,)
