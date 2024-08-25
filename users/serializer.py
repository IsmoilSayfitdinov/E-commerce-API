from typing import Any, Dict
from rest_framework import serializers
from users.models import UserModel, NEW
from rest_framework import status
from shared.utils import send_to_email_code
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.password_validation import validate_password


class Userserializers(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ["id","username", "is_staff", "is_superuser", "avatar"]


class UserRegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)
    uuid = serializers.IntegerField(read_only=True)
    auth_status = serializers.CharField(read_only=True, required=False)
    
    class Meta:
        model = UserModel
        fields = ["uuid", "auth_status", "first_name", "last_name", "username", "email", "password", "confirm_password"]
        
    def validate(self, attrs):
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs
    
    def create(self, validated_data):
        validated_data.pop("confirm_password")
        
        user = super(UserRegistrationSerializer, self).create(validated_data)
        code = user.create_verify_code()
        
        send_to_email_code(user.email, code)
        user.set_password(validated_data["password"])
        user.save()
        return user
    
    
    def to_representation(self, instance):
        data = super(UserRegistrationSerializer, self).to_representation(instance)
        data['access_token'] = instance.get_token()['access']
        data["auth_status"] = NEW
        return data
    
class LoginSerializer(TokenObtainPairSerializer):
    
    password = serializers.CharField(max_length=128, required=True, write_only=True)
    
    
    def validate(self, attrs):
        username = attrs["username"]
        password = attrs["password"]
        
        user = UserModel.objects.filter(username=username).first()
        
        if user is None:
            raise serializers.ValidationError({"username": "User not found"})
        
        auth_user = authenticate(username=username, password=password)
        
        if not auth_user:
            raise serializers.ValidationError({"password": "Password is incorrect"})
        
        refresh = RefreshToken.for_user(auth_user)
        
        response = {
			"status": True,
			"access_token": str(refresh.access_token),
			"refresh_token": str(refresh)
		}
        
        return response
    
class UserForgetPasswordForemailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    

class UserResetPasswordSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    password = serializers.CharField(max_length=128, required=True)
    confirm_password = serializers.CharField(max_length=128, required=True)
    
    class Meta:
        model = UserModel
        fields = ["id","password", "confirm_password"]
    
    def validate(self, attrs):
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError({"password": "Password fields wrong"})
        
        if attrs["password"]:
            validate_password(attrs["password"])
            
        return attrs
    
    
    def update(self, instance, validated_data):
        password = validated_data.pop("password")
        instance.set_password(password)
        return super(UserResetPasswordSerializer, self).update(instance, validated_data)
    
    
    
class UserUpdateSerializer(serializers.ModelSerializer):
     class Meta:
        model = UserModel
        fields = ['first_name', 'last_name', 'email', "username"]