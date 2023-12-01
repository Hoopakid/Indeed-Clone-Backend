from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import RegisterAPIView, LogoutAPIView, UserInfoAPIView, FacebookLogin, GoogleLogin, \
    RedirectToGoogleAPIView, GithubLogin, callback, callback_github, ContactCreateAPIView, ContactUpdateDestroyAPIView

urlpatterns = [
    # user registration APIs
    path('register', RegisterAPIView.as_view(), name='register'),
    path('logout', LogoutAPIView.as_view(), name='logout'),
    path('profile', UserInfoAPIView.as_view(), name='user-info'),

    # CRUD API of user data
    path('contact-create', ContactCreateAPIView.as_view(), name='contact-create'),
    path('contact-update/<int:user_id>', ContactUpdateDestroyAPIView.as_view(), name='contact-update'),

    # drj-jwt
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # sign with social
    path('facebook', FacebookLogin.as_view(), name='fb_login'),
    path('google', GoogleLogin.as_view(), name='google_login'),
    path('google-login', RedirectToGoogleAPIView.as_view(), name='google_login2'),
    path('github', GithubLogin.as_view(), name='github_login'),
    path('google/callback', callback, name='google_callback'),
    path('github/callback', callback_github, name='github_callback')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
