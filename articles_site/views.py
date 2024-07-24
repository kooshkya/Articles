from django.contrib.auth import login, logout
from django.shortcuts import render
from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from . import serializers, models
from .models import Article
from .pagination import MyPagination

from django.contrib.auth.decorators import login_required


@login_required
def landing_view(request):
    return render(request, 'articles_site/landing.html')


@login_required
def article_detail_view(request, pk):
    return render(request, 'articles_site/article_detail.html', {'article_id': pk})


def signup_view(request):
    return render(request, "articles_site/signup.html")


def login_view(request):
    return render(request, "articles_site/login.html")


class RatingCreateUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = serializers.RatingSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            article_id = serializer.validated_data['article_id']
            rating_value = serializer.validated_data['rating']

            try:
                article = Article.objects.get(id=article_id)
            except Article.DoesNotExist:
                return Response({"detail": "Article not found."}, status=status.HTTP_404_NOT_FOUND)

            rating, created = models.Rating.objects.update_or_create(
                user=user,
                article=article,
                defaults={'rating': rating_value}
            )

            return Response({
                'article_id': rating.article.id,
                'rating': rating.rating,
                'created': created
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArticleListCreateAPI(generics.ListCreateAPIView):
    serializer_class = serializers.ArticleSerializer
    queryset = Article.objects.all()

    permission_classes = [IsAuthenticated]
    pagination_class = MyPagination

    def create(self, request, *args, **kwargs):
        request.data.update({"author": request.user.id})
        return super().create(request, *args, **kwargs)


class ArticleRetrieveAPI(generics.RetrieveAPIView):
    serializer_class = serializers.ArticleSerializer
    queryset = Article.objects.all()

    permission_classes = [IsAuthenticated]


class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = serializers.LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)
            return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            logout(request)
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class SignupView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = serializers.SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            login(request, user)
            return Response({"message": "User created successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
