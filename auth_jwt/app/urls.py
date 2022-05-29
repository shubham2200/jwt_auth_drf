
from django.contrib import admin
from django.urls import path
from .views import *
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('', UserRegister.as_view() , name='register' ),
    path('login/', UserLoginView.as_view(), name='login'),
    path('home/', home.as_view(), name='home'),
    path('list/', SearchProductListAPIView.as_view(), name='list'),




]
