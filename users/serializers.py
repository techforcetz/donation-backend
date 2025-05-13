from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import Users

class Register_Serializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only = True)

    class Meta:
        model = Users
        fields = ["username","email","phone","password","confirm_password"]

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password_error":"passwords do not match"})
        return attrs
    
    def create(self, validated_data):
        validated_data.pop("confirm_password")
        user = Users(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

class Login_Serializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if not username or not password:
            raise serializers.ValidationError({"error":"username and password must be provided"})
        
        user = authenticate(username = username , password = password)

        if not user:
            raise serializers.ValidationError({"error":"wrong credentials"})
        
        attrs['user'] = user

        return attrs