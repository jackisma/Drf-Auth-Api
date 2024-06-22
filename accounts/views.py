from django.shortcuts import render
from rest_framework.response import Response 
from rest_framework.views import APIView
from .serializers import *
from rest_framework import status
from django.contrib.auth import authenticate
from .renderers import UserRenderer 
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated


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
        





# User Profile View Class 
class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def get(self, request , format=None):
        user = request.user 
        serializer = UserProfileSerializer(user)
        return Response(serializer.data,status=status.HTTP_200_OK)





# User Change Password Class 
class UserChangePasswordView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def post (self,request,format=None):
        serializer = UserChangePasswordSerializer(data=request.data,context={'user':request.user})
        if serializer.is_valid():
            return Response({"msg":"password changed successfully"} ,status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
