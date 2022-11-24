from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .import views

urlpatterns = [
    path('token/', views.CustomTokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('user/', views.UserAPIView.as_view()),
    path('user/<int:pk>/', views.UserAPIView.as_view()),
]
