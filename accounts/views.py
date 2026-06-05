from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from django.utils import timezone
from datetime import timedelta
from accounts.models import User, PasswordResetOTP
from accounts.serializers import UserSerializer, CustomTokenObtainPairSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from utils.genotpcode import random_with_N_digits
from utils.sendemail import send_email
from django.utils import timezone
from datetime import timedelta


class UserViewSet(viewsets.ModelViewSet):
    """Admin-only: manage all users"""
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

    @action(detail=False, methods=['get', 'patch'], permission_classes=[IsAuthenticated])
    def me(self, request):
        if request.method == 'GET':
            return Response(UserSerializer(request.user).data)
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({'message': 'User registered successfully', 'user_id': user.id}, status=status.HTTP_201_CREATED)


class LoginMixin(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = CustomTokenObtainPairSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class RequestPasswordResetView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'User with this email does not exist'}, status=status.HTTP_404_NOT_FOUND)

        code = str(random_with_N_digits(6))

        # Upsert: one OTP per user at a time, expires in 10 minutes
        PasswordResetOTP.objects.update_or_create(
            user=user,
            defaults={'code': code, 'expires_at': timezone.now() + timedelta(minutes=10)}
        )

        try:
            send_email(user.full_name, code, "Password Reset Request", user.email, "emails/resetpasswordotp_email.html")
        except Exception:
            PasswordResetOTP.objects.filter(user=user).delete()
            return Response({'error': 'Failed to send OTP email. Please try again.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'message': 'Password reset OTP sent to your email'}, status=status.HTTP_200_OK)


class ResetPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        code = request.data.get('code')
        new_password = request.data.get('new_password')

        if not all([email, code, new_password]):
            return Response({'error': 'Email, code, and new_password are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        try:
            otp = PasswordResetOTP.objects.get(user=user, code=code)
        except PasswordResetOTP.DoesNotExist:
            return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)

        if otp.expires_at < timezone.now():
            otp.delete()
            return Response({'error': 'OTP has expired. Please request a new one.'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()

        # Delete OTP immediately — it's gone after one use
        otp.delete()

        return Response({'message': 'Password reset successfully'}, status=status.HTTP_200_OK)
