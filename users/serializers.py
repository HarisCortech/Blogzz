from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import CustomUser, Profile

class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer class to serialize registration requests and create a new user.
    """

    class Meta:
        model = CustomUser
        fields = ("id", "username", "email", "password")
        extra_kwargs = {"password": {"write_only": True}} 

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)

class UserLoginSerializer(serializers.Serializer):
    
    """
    Serializer class to serialize login requests of a user.
    """
    email = serializers.EmailField()
    password = serializers.CharField(write_only = True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")

class CustomUserSerializer(serializers.ModelSerializer):
    """
    Serializer class to serialize CustomUser model.
    """
    
    class Meta:
        model = CustomUser
        fields = ('id','email','password')


# This is for updating and creating user profile, since Profile is in one-to-one relation with User
# We are inheriting CustomUserSerializer, so we can serialize the profile with the user info
class ProfileSerializer(CustomUserSerializer):
    class Meta:
        model = Profile
        fields = ("bio",)

class ProfileAvatarSerializer(serializers.ModelSerializer):
    """
    Serializer class to serialize the avatar
    """
    
    class Meta:
        model = Profile
        fields = ("avatar",)