from django.shortcuts import render
from rest_framework.response import Response 
from rest_framework.views import APIView
from .serializers import UserRegisterSerializer, UserLoginSerializer
from rest_framework import status
from django.contrib.auth import authenticate
from .renderers import UserRenderer 
from rest_framework_simplejwt.tokens import RefreshToken


# Json Web Token For Each User. 
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


# Sign Up Class View 
class UserCreation(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response({"token":token ,"msg":"You registered successfuly!"},status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


# Login Class View 
class LoginView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email,password=password)
            if user is not None:
                token = get_tokens_for_user(user)
                return Response({"token":token,"msg" : "Login Successful"} , status=status.HTTP_200_OK)
            else:
                return Response({"errors":"Login Faild , Email or Password is not valid !"} , status=status.HTTP_404_NOT_FOUND)
            
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
