from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import AbstractUser


class ArticlesUser(AbstractUser):
    created_at = models.DateTimeField(auto_now_add=True)


class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    average_rating = models.FloatField(default=0)
    rates_count = models.IntegerField(default=0)
    ratings = models.ManyToManyField(get_user_model(), through='Rating', related_name='rated_articles')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Rating(models.Model):
    RATING_CHOICES = [
        (0, '0'),
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    ]

    class Meta:
        unique_together = ('user', 'article')

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
