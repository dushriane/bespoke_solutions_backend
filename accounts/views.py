from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from accounts.models import User, VerificationCode
from accounts.serializers import (
    UserSerializer, 
    CustomTokenObtainPairSerializer,
    VerifyAccountSerializer,
    RequestPasswordResetSerializer,
    ResetPasswordSerializer
)
from rest_framework.permissions import IsAuthenticated, AllowAny
from utils.genotpcode import random_with_N_digits
from utils.sendemail import send_email
from drf_yasg.utils import swagger_auto_schema
from django.utils import timezone
from datetime import timedelta

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer

class LoginMixin(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=CustomTokenObtainPairSerializer)
    def post(self, request, *args, **kwargs):
        # email = request.data.get('email')
        # password = request.data.get('password')

        serializer = CustomTokenObtainPairSerializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.validated_data, status=status.HTTP_200_OK)

# class VerifyAccountView(APIView):
#     permission_classes = [AllowAny]
    
#     @swagger_auto_schema(request_body=VerifyAccountSerializer)
#     def post(self, request, *args, **kwargs):
#         email = request.data.get('email')
#         code = request.data.get('code')
        
#         if not email or not code:
#             return Response({'error': 'Email and code are required'}, status=status.HTTP_400_BAD_REQUEST)
            
#         try:
#             user = User.objects.get(email=email)
#             verification = VerificationCode.objects.filter(
#                 user=user, 
#                 code=code, 
#                 purpose='verification',
#                 is_verified=False
#             ).last()
            
#             if not verification:
#                 return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
            
#             if verification.is_expired():
#                 return Response({'error': 'OTP has expired. Please request a new verification code.'}, status=status.HTTP_400_BAD_REQUEST)
                
#             verification.is_verified = True
#             verification.save()
            
#             user.is_active = True
#             user.save()
            
#             return Response({'message': 'Account verified successfully'}, status=status.HTTP_200_OK)
#         except User.DoesNotExist:
#             return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

class RequestPasswordResetView(APIView):
    permission_classes = [AllowAny]
    
    @swagger_auto_schema(request_body=RequestPasswordResetSerializer)
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        if not email:
            return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            user = User.objects.get(email=email)
            code = random_with_N_digits(4)
            expires_at = timezone.now() + timedelta(minutes=10)
            VerificationCode.objects.create(
                user=user, 
                code=code,
                purpose='reset',
                expires_at=expires_at
            )
            
            send_email(user.full_name, code, "Password Reset Request", user.email, "emails/resetpasswordotp_email.html")
            
            return Response({'message': 'Password reset OTP sent to email'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User with this email does not exist'}, status=status.HTTP_404_NOT_FOUND)

class ResetPasswordView(APIView):
    permission_classes = [AllowAny]
    
    @swagger_auto_schema(request_body=ResetPasswordSerializer)
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        code = request.data.get('code')
        new_password = request.data.get('new_password')
        
        if not all([email, code, new_password]):
            return Response({'error': 'Email, code, and new_password are required'}, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            user = User.objects.get(email=email)
            verification = VerificationCode.objects.filter(
                user=user, 
                code=code, 
                purpose='reset',
                is_verified=False
            ).last()
            
            if not verification:
                return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
            
            if verification.is_expired():
                return Response({'error': 'OTP has expired. Please request a new reset code.'}, status=status.HTTP_400_BAD_REQUEST)
                
            user.set_password(new_password)
            user.save()
            
            verification.is_verified = True
            verification.save()
            
            return Response({'message': 'Password reset successfully'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)