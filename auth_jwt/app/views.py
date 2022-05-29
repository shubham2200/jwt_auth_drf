from django.shortcuts import render

# Create your views here.
from django.contrib.auth import authenticate
from .render import UserRenderer
from .seri import *
from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken    
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination

# from rest_framework.permissions import IsAuthenticated
# Create your views here.


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class UserRegister(APIView):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    # permission_classes = [IsAuthenticated]
    def post(self, request ,format=None):
        serializer = Seri_user(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user= serializer.save()
            token = get_tokens_for_user(user)
            return JsonResponse({
             "data":serializer.data ,
            "access":token
             })
        else:
            return JsonResponse(serializer.errors)
class UserLoginView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get('email')
        password = serializer.data.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            token = get_tokens_for_user(user)
            return JsonResponse({'token':token, 'msg':'Login Success'})
        else:
            return JsonResponse({'error':'error'})
      

class home(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        seri = ProductSeri(data=request.data)
        if seri.is_valid(raise_exception=True):
            seri.save()
            return JsonResponse({'yess': seri.data})
        else:
            return JsonResponse({'task':'not done'})
    def get(self, request, *args, **kwargs):
        seri = Product.objects.all()
        data = ProductSeri(seri , many=True)
        list_data = data.data
        return JsonResponse({'All data':list_data })


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 6


class SearchProductListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    queryset = Product.objects.all()
    serializer_class = ProductSeri
    filter_backends = [filters.SearchFilter]
    pagination_class = StandardResultsSetPagination
    search_fields = ['product_name','id']
    ordering = ['product_name']


