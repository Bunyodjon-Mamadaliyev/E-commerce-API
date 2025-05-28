from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import verification_codes
from .views import (AuthorizeView, VerifyView, LoginView, LogoutView,
    ForgotPasswordView, ResetPasswordView, SendCodeView, UserProfileView)

verification_codes["+998972088804"] = "888888"

urlpatterns = [
    path("authorize/", AuthorizeView.as_view()),
    path("verify/", VerifyView.as_view()),
    path("login/", LoginView.as_view()),
    path("logout/", LogoutView.as_view()),
    path("token/refresh/", TokenRefreshView.as_view(), name='token_refresh'),
    path("forgot-password/", ForgotPasswordView.as_view()),
    path("reset-password/", ResetPasswordView.as_view()),
    path("send-code/", SendCodeView.as_view()),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
]
