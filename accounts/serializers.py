from rest_framework import serializers
from accounts.models import User, VerificationCode
from utils.genotpcode import random_with_N_digits
from utils.sendemail import send_email
import datetime
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserSerializer(serializers.ModelSerializer):
    re_enter_password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['id', 'email', 'full_name', 'phone_number', 'password', 're_enter_password', 'is_active', 'created_at']
        read_only_fields = ('id', 'date_joined')
        extra_kwargs = {
            "password": {"write_only": True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['re_enter_password']:
            raise serializers.ValidationError({"password": "Password and re-entered password do not match."})
        
        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError({"email": "Email already exists."})
        return attrs
    
    def create(self,validated_data):
        re_enter_password = validated_data.pop('re_enter_password')
        user = User.objects.create_user(**validated_data)
        ver=VerificationCode.objects.create(user=user, code=random_with_N_digits(4))

        send_email(user.full_name, ver.code, "Account Verification Code", user.email, "emails/accountverification_email.html")
        return user
    
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        User.objects.filter(id=user.id).update(last_login=datetime.datetime.now())
        user.save()
        token = super().get_token(user)
        token['email'] = user.email
        token['full_name'] = user.full_name
        token['phone_number'] = user.phone_number
        token['user_type'] = user.user_type
        return token