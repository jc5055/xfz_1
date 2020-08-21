from rest_framework import serializers
from .models import News, NewsCategory, Comment, Banner
from apps.xfzauth.serializers import AuthSerializer


class NewsCategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = NewsCategory
        fields = ('id', 'name')


class NewsSerializer(serializers.ModelSerializer):
    category = NewsCategorySerializers()
    author = AuthSerializer()

    class Meta:
        model = News
        fields = ('id', 'title', 'desc', 'thumbnail', 'pub_time', 'category', 'author')


class NewsCommentSerializer(serializers.ModelSerializer):
    author = AuthSerializer()

    class Meta:
        model = Comment
        fields = ('id', 'content', 'pub_time', 'author')


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ('id', 'priority', 'image_url', 'link_to')
