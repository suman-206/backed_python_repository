from rest_framework import serializers
from .models import  CustomUser
from django.contrib.auth import authenticate

import logging

logger = logging.getLogger("my_project")

class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'email', 'mobile_number', 'password']

    def create(self, validated_data):
        """Handles user creation with hashed password"""
        try:
            logger.info(f"Creating new user: {validated_data['email']}")
            user = CustomUser.objects.create_user(**validated_data)
            return user

        except Exception as e:
            logger.critical(f"Error creating user: {str(e)}", exc_info=True)
            raise serializers.ValidationError({"error": "Failed to create user. Please try again."})



class LoginSerializer(serializers.Serializer):
    identifier = serializers.CharField(required=True)  # Can be email, username, or mobile number
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        identifier = attrs.get("identifier")  # General field (email, username, or mobile)
        password = attrs.get("password")

        if not identifier or not password:
            raise serializers.ValidationError("Both identifier and password are required.")

        # Check if identifier is email, username, or mobile number
        user = None
        if CustomUser.objects.filter(email=identifier).exists():
            user = CustomUser.objects.get(email=identifier)
        elif CustomUser.objects.filter(username=identifier).exists():
            user = CustomUser.objects.get(username=identifier)
        elif CustomUser.objects.filter(mobile_number=identifier).exists():
            user = CustomUser.objects.get(mobile_number=identifier)
        print("user :",user)
        print("pass",password)
        if user:
            try:
                authenticated_user = authenticate(username=user, password=password)
                print("authenticated_user",authenticated_user)
                if authenticated_user:
                    attrs["user"] = authenticated_user
                    return attrs
            except Exception as e:
                print("exception :",{e})

        raise serializers.ValidationError("Invalid credentials.")


# from django.contrib.auth import get_user_model
#
# User = get_user_model()
#
# class RegistrationSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True, min_length=8)
#
#     class Meta:
#         model = User
#         fields = ["first_name", "last_name", "username", "email", "mobile_number", "password"]
#         extra_kwargs = {"email": {"validators": []}}  # Remove default UniqueValidator to avoid redundant DB hits
#
#     def create(self, validated_data):
#         user = User.objects.create_user(**validated_data)
#         return user
