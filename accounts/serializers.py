from rest_framework import serializers
from accounts.models import User
import datetime
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserSerializer(serializers.ModelSerializer):
    re_enter_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'full_name', 'phone_number', 'password', 're_enter_password', 'is_active', 'created_at']
        read_only_fields = ('id', 'created_at')
        extra_kwargs = {
            "password": {"write_only": True}
        }

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('re_enter_password'):
            raise serializers.ValidationError({
                "password": "Password and re-entered password do not match."
                })
        if User.objects.filter(email=attrs.get('email')).exists():
            raise serializers.ValidationError({
                "email": "Email already exists."
                })
        return attrs

    def create(self, validated_data):
        validated_data.pop('re_enter_password')
        return User.objects.create_user(**validated_data)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    username = None 

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        try:
            user = User.objects.get(email=email)
            if not user.check_password(password):
                raise serializers.ValidationError({
                    'password':'Invalid credentials'
                    })
            attrs['users'] = user
        except User.DoesNotExist:
            raise serializers.ValidationError({
                'email':'User not found'
                })
        
        tokens = self.get_token(user)
        
        return {
            'refresh': str(tokens),
            'access': str(tokens.access_token),
        }

    @classmethod
    def get_token(cls, user):
        User.objects.filter(id=user.id).update(last_login=datetime.datetime.now())
        token = super().get_token(user)
        token['email'] = user.email
        token['full_name'] = user.full_name
        token['phone_number'] = user.phone_number
        token['user_type'] = user.user_type
        return token
