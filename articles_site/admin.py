from django.contrib import admin
from .models import Article, Rating, ArticlesUser
from django.contrib.auth import get_user_model

User = get_user_model()


class RatingInline(admin.TabularInline):
    model = Rating
    extra = 1


@admin.register(ArticlesUser)
class ArticlesUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'created_at')
    search_fields = ('username', 'email')


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author')
    search_fields = ('title', 'author')
    list_filter = ('author',)
    inlines = [RatingInline]


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('article', 'user', 'rating')
    list_filter = ('rating', 'user', 'article')
    search_fields = ('user__username', 'article__title')
    autocomplete_fields = ['user', 'article']