from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .serializers import( AuthorizeSerializer, VerifySerializer, LoginSerializer,
        ForgotPasswordSerializer, ResetPasswordSerializer, UserSerializer)

verification_codes = {}

class AuthorizeView(generics.GenericAPIView):
    serializer_class = AuthorizeSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            field, errors = list(serializer.errors.items())[0]
            return Response({
                "success": False,
                "error": {
                    "code": "INVALID_REQUEST",
                    "message": "The provided data is invalid",
                    "details": {
                        "field": field,
                        "message": errors[0]
                    }
                }
            }, status=status.HTTP_400_BAD_REQUEST)
        phone = serializer.validated_data['phone']
        code = "888888"
        verification_codes[phone] = code
        return Response({
            "success": True,
            "message": f"Verification code sent to {phone}"
        }, status=status.HTTP_200_OK)


class VerifyView(generics.GenericAPIView):
    serializer_class = VerifySerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            field, errors = list(serializer.errors.items())[0]
            return Response({
                "success": False,
                "error": {
                    "code": "INVALID_REQUEST",
                    "message": "The provided data is invalid",
                    "details": {
                        "field": field,
                        "message": errors[0]
                    }
                }
            }, status=status.HTTP_400_BAD_REQUEST)
        phone = serializer.validated_data['phone']
        code = serializer.validated_data['code']
        password = serializer.validated_data.get('password')
        name = serializer.validated_data.get('name', '')
        expected_code = verification_codes.get(phone)
        if expected_code is None:
            return Response({
                "success": False,
                "error": {
                    "code": "CODE_NOT_FOUND",
                    "message": "No verification code was sent for this phone.",
                    "details": {
                        "field": "code",
                        "message": "Verification code not found"
                    }
                }
            }, status=status.HTTP_400_BAD_REQUEST)
        if expected_code != code:
            return Response({
                "success": False,
                "error": {
                    "code": "INVALID_CODE",
                    "message": "Invalid verification code",
                    "details": {
                        "field": "code",
                        "message": "Code does not match"
                    }
                }
            }, status=status.HTTP_400_BAD_REQUEST)
        email = f"{phone.replace('+', '')}@example.com"
        user, created = User.objects.get_or_create(phone=phone,defaults={'name': name, 'email': email})
        if password:
            user.set_password(password)
            user.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            "success": True,
            "data": {
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh),
                "expires_in": 3600
            }
        }, status=status.HTTP_200_OK)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            field, errors = list(serializer.errors.items())[0]
            return Response({
                "success": False,
                "error": {
                    "code": "INVALID_REQUEST",
                    "message": "The provided data is invalid",
                    "details": {
                        "field": field,
                        "message": errors[0]
                    }
                }
            }, status=status.HTTP_400_BAD_REQUEST)
        phone = serializer.validated_data["phone"]
        password = serializer.validated_data["password"]
        try:
            user = User.objects.get(phone=phone)
        except User.DoesNotExist:
            return Response({
                "success": False,
                "error": {
                    "code": "INVALID_CREDENTIALS",
                    "message": "Invalid phone or password",
                    "details": {
                        "field": "phone",
                        "message": "User not found"
                    }
                }
            }, status=status.HTTP_401_UNAUTHORIZED)

        if not user.check_password(password):
            return Response({
                "success": False,
                "error": {
                    "code": "INVALID_CREDENTIALS",
                    "message": "Invalid phone or password",
                    "details": {
                        "field": "password",
                        "message": "Incorrect password"
                    }
                }
            }, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        return Response({
            "success": True,
            "data": {
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh),
                "expires_in": 3600
            }
        }, status=status.HTTP_200_OK)


class LogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"status": True, "message": "Successfully logged out"})
        except Exception:
            return Response({"status": False, "message": "Invalid token"}, status=400)


class ForgotPasswordView(generics.GenericAPIView):
    serializer_class = ForgotPasswordSerializer
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data['phone']
        user = User.objects.get(phone=phone)
        import random
        code = str(random.randint(100000, 999999))
        verification_codes[phone] = code
        print(f"[DEBUG] Verification code for {phone}: {code}")
        return Response({
            "success": True,
            "message": f"Password reset code sent to {phone}"
        }, status=status.HTTP_200_OK)


class ResetPasswordView(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data['phone']
        code = serializer.validated_data['code']
        new_password = serializer.validated_data['new_password']
        expected_code = verification_codes.get(phone)
        if expected_code != code:
            return Response({
                "success": False,
                "error": {
                    "code": "INVALID_CODE",
                    "message": "Invalid verification code",
                    "details": {
                        "field": "code",
                        "message": "Verification code does not match"
                    }
                }
            }, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(phone=phone)
        except User.DoesNotExist:
            return Response({
                "success": False,
                "error": {
                    "code": "INVALID_REQUEST",
                    "message": "The provided data is invalid",
                    "details": {
                        "field": "phone",
                        "message": "User not found"
                    }
                }
            }, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(new_password)
        user.save()
        verification_codes.pop(phone, None)
        return Response({
            "success": True,
            "message": "Password reset successful"
        }, status=status.HTTP_200_OK)


class SendCodeView(APIView):
    def post(self, request):
        phone = request.data.get("phone")
        code = "888888"
        verification_codes[phone] = code
        return Response({"success": True, "code": code})


class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object(), data=request.data, partial=True)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response({"success": True, "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({
            "success": False,
            "error": {
                "code": "INVALID_REQUEST",
                "message": "The provided data is invalid",
                "details": serializer.errors
            }
        }, status=status.HTTP_400_BAD_REQUEST)
