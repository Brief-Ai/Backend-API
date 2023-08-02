from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import serializers
import re

class UserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def validate_password(self, value):
        # Add basic password requirements
        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError("Password must contain at least one uppercase letter.")
        if not re.search(r'[a-z]', value):
            raise serializers.ValidationError("Password must contain at least one lowercase letter.")
        if not re.search(r'[0-9]', value):
            raise serializers.ValidationError("Password must contain at least one digit.")
        return value
    
    def validate(self, data):
        # Check if the passwords match
        password = data['password']
        password2 = data['password2']
        
        if password != password2:
            raise serializers.ValidationError({"password": ["Passwords do not match."]})
        
        # Miniumum password length of 6
        if len(password) < 6:
            raise serializers.ValidationError({"password": ["Password must be at least 6 characters long."]})

        # Check if the username already exists
        username = data['username']
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError({"username": ["A user with that username already exists."]})

        return data
    
    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']
        
        account = User(username=username)
        account.set_password(password)
        account.save()
        
        return account

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect credentials")

class TokenSerializer(serializers.Serializer):
    token = serializers.CharField()