from ast import If
from pyexpat import model
from tokenize import Name
from .models import *
from rest_framework import serializers
from django.contrib.auth.hashers import make_password


class Seri_user(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

    def validate(self,attrs):
        email = attrs.get('email')
        Name = attrs.get('name')
        password = attrs.get('password')
        phone = attrs.get('phone')
        pincode = attrs.get('pincode')
        if "10" >= phone :
            raise serializers.ValidationError('enter number 10 degites')
        elif pincode >= "6":
            raise serializers.ValidationError('enter pincode 6 degites')

        return attrs

    def create(self, validated_data):
        pas = validated_data['password']
        user = User.objects.create(
            email=validated_data['email'],
            name=validated_data['name'],
            password=make_password( pas),
            phone=validated_data['phone'],
            pincode=validated_data['pincode']

        )
        return user


class UserLoginSerializer(serializers.ModelSerializer):
  email = serializers.EmailField(max_length=255)
  class Meta:
    model = User
    fields = ['email', 'password']

class ProductSeri(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'