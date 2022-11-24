from rest_framework import serializers
from .models import CustomUser
from django.conf import settings
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from datetime import datetime, timedelta

class CustomJWTSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        current_time = datetime.now()
        data['access_validity'] = str(current_time + settings.SIMPLE_JWT.get('ACCESS_TOKEN_LIFETIME'))
        data['refresh_validity'] = str(current_time + settings.SIMPLE_JWT.get('REFRESH_TOKEN_LIFETIME'))
        return data
    
    
    
class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    user_name = serializers.CharField()
    password = serializers.CharField(min_length=8, write_only=True)
    class Meta:
        model = CustomUser
        # extra_kwargs = {'password':{'write_only':True}}
        fields = ['id', 'user_name', 'first_name', 'email', 'role', 'password', 'start_date', 'phone', 'is_staff', 'is_active', 'is_superuser']
        
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    
    
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            setattr(instance, attr, value)
            
            instance.save()
            return instance
                