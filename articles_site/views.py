from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from . import serializers
from .models import Article, Rating
from .pagination import MyPagination
from .permissions import IsAuthenticatedAndRegisteredOver10Days
from .throttles import DailyUserRatingThrottle


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


class RatingAPI(APIView):
    permission_classes = [IsAuthenticated, IsAuthenticatedAndRegisteredOver10Days]
    throttle_classes = [DailyUserRatingThrottle]

    def post(self, request, *args, **kwargs):
        serializer = serializers.RatingSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            rating_value = serializer.validated_data['rating']
            article = serializer.validated_data['article']

            qs = Rating.objects.filter(user=user, article=article)
            created = False
            rating = None
            if qs.exists():
                rating = qs.first()
                article.average_rating = (
                                                 article.average_rating * article.rates_count - rating.rating + rating_value) / article.rates_count
                rating.rating = rating_value
                rating.save()
                created = False
            else:
                rating = Rating.objects.create(article=article, user=user, rating=rating_value)
                article.average_rating = (article.average_rating * article.rates_count + rating_value) / (
                        article.rates_count + 1)
                article.rates_count += 1
                created = True
            article.save()

            return Response({
                'article_id': rating.article.id,
                'rating': rating.rating,
                'created': created
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetUserRatingView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        article_id = request.query_params.get('article_id')
        if not article_id:
            return Response("You need to specify the article_id in URL kwargs", status=status.HTTP_400_BAD_REQUEST)
        qs = Rating.objects.filter(user=request.user, article_id=article_id)
        if qs.exists():
            serializer = serializers.RatingSerializer(qs.first())
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response("You haven't rated this article", status=status.HTTP_404_NOT_FOUND)


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
