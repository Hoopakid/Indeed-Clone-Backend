from django.contrib.auth import get_user_model
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import UserSerializer, ResumeSerializer

User = get_user_model()


class RegisterAPIView(GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]

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
            return Response({'success': False, 'message': 'Passwords are not same!'}, status=400)


class LogoutAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        refresh_token = request.data.get('refresh')
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response(status=204)


class UserInfoAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        user_serializer = UserSerializer(user)
        return Response(user_serializer.data)


# THIS IS THE ANOTHER WAY FOR CreateResumeView
# class CreateResumeView(CreateAPIView):
#     serializer_class = ResumeSerializer
#     permission_classes = [IsAuthenticated]
#
#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)


class CreateResumeView(GenericAPIView):
    permission_classes = ()
    serializer_class = ResumeSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)
