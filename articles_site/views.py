from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import login
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from . import serializers


def signup_view(request):
    return render(request, "articles_site/signup.html")


class SignupView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = serializers.SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            login(request, user)
            return Response({"message": "User created successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def test_view(request):
    return HttpResponse("This is a test view")
