from django.shortcuts import render
from .models import CustomUser
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from django.db.models import Count
from rest_framework import status
from .serializers import UserSerializer

# Create your views here.

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        token['user_name'] = user.user_name
        
        return token

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    

class UserAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def get(self, request, format=None):
        if request.method == 'GET':
            
            users = CustomUser.objects.filter(is_superuser=False)
            
            serializer= UserSerializer(users, many=True)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response ({'error':'No user'}, status= status.HTTP_400_BAD_REQUEST)
    def post(self, request, format=None):
        if request.method == 'POST':
            serializer = UserSerializer(data= request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        return Response({'error':'cannot create user'})
    
    def delete(self, request, pk, format=None):
        if request.method == 'DELETE':
            user = CustomUser.objects.filter(id=pk)
            user.delete()
            
            return Response({'message':'success'})
        return Response({'error':'cannot delete'})
    
