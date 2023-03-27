from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    access_token = serializers.SerializerMethodField()

    def get_access_token(self, obj):
        refresh = RefreshToken.for_user(obj)
        return {
            # 'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        fields = ('username', 'password', 'access_token')


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        # Add extra user info to token payload
        data['user_id'] = self.user.id
        data['email'] = self.user.email
        return data
