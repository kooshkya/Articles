# serializers.py

from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate

from articles_site import models


class ArticleSerializer(serializers.ModelSerializer):
    author_username = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Article
        fields = ('id', 'title', 'content', 'author', 'author_username', 'average_rating', 'rates_count')
        read_only_fields = ('id', 'author_username', 'average_rating', 'rates_count')

    def get_author_username(self, obj):
        return obj.author.username

    def to_representation(self, instance):
        result = super().to_representation(instance)
        result.pop("author", None)
        return result


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Rating
        fields = ('id', 'article', 'user', 'rating')
        read_only_fields = ('id', 'user')


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                data['user'] = user
            else:
                raise serializers.ValidationError("Invalid credentials")
        else:
            raise serializers.ValidationError("Both username and password are required")
        return data


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
