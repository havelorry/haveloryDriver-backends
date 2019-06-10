from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializations import ProfileDetailSerializer,ProfileSerializer
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth import authenticate

# Create your views here.

class DriverPofile(APIView):
    def post(self,request,format=None):
        print ("inside post method")
        profile_serializer=ProfileSerializer(data=request.data)
        if profile_serializer.is_valid(raise_exception=True):
            user=profile_serializer.save()
            if user:
                token = Token.objects.create(user=user)
                print("token created",token)
            profile_detail_serializer=ProfileDetailSerializer(data=request.data)
            
            if profile_detail_serializer.is_valid(raise_exception=True):
                
                profile_detail_serializer.save()
                return Response({"massage":"saved successfully"})
        return Response("done")

class Login(APIView):
    def post(self,request,format=None):
        username = request.data.get("username")
        password = request.data.get("password")
        if username is None or password is None:
            return Response({'error': 'Please provide both username and password'},
                            status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(username=username, password=password)
        print(user)
        if not user:
            return Response({'error': 'Invalid Credentials'},
                            status=status.HTTP_404_NOT_FOUND)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"massage":"Login Successfully","token":token.key})
    #def get(self,request,format=None):








