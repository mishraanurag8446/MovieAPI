from .models import Collection, Movie
from rest_framework import serializers
from django.contrib.auth.models import User


# class RegistrationSerializer(serializers.ModelSerializer):
#     # password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
#
#     class Meta:
#         model = User
#         fields = ['username', 'password']
#         extra_kwargs = {
#             'password': {'write_only': True}
#         }
#
#     def save(self):
#         user = User(
#             username=self.validated_data['username']
#         )
#         password = self.validated_data['password']
#         # password2 = self.validated_data['password2']
#
#         # if password != password2:
#         # raise serializers.ValidationError({'password': 'Passwords must match.'})
#
#         user.set_password(password)
#         user.save()
#         return user


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = '__all__'


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['title', 'description', 'genres', 'uuid']
