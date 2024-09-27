from django.shortcuts import render
from .models import ProductType,Product
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import GenericAPIView
from .serializers import ProductTypeSerializer,ProductSerializer,UserSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

# Create your views here.

@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response('Registered succesfully')
    else:
        return Response(serializer.errors)

@api_view(['POST'])
@permission_classes([])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')
    user = authenticate(username=email,password=password)
    if user == None:
        return Response('Invalid credentials')
    else:
        token,_ = Token.objects.get_or_create(user=user)
        return Response(token.key)

class ProductTypeApiView(ModelViewSet):
    queryset = ProductType.objects.all()
    serializer_class = ProductTypeSerializer

class ProductApiView(GenericAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get(self,request):
        product_objs = Product.objects.all()
        serializer = ProductSerializer(product_objs,many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response('Data created')
        else:
            return Response(serializer.errors)

class ProductDetailApiView(GenericAPIView):
    queryset = Product.objects.all() 
    serializer_class = ProductSerializer

    def get(self,request,pk):
        try:
            product_obj = Product.objects.get(id=pk)
        except:
            return Response('Data not found!')
        serializer = ProductSerializer(product_obj)
        return Response(serializer.data)
    
    def put(self,request,pk):
        try:
            product_obj = Product.objects.get(id=pk)
        except:
            return Response('Data not found!')
        
        serializer = ProductSerializer(product_obj,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response('Data updated!')
        else:
            return Response(serializer.errors)
        
    def delete(self,request,pk):
        try:
            product_obj = Product.objects.get(id=pk)
        except:
            return Response('Data not found!')
        product_obj.delete()
        return Response('Data deleted!')
        