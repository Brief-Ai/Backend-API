from rest_framework import serializers
from .models import Search, Article

class SearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Search
        fields = ['user', 'query', 'timestamp']



class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'title', 'description', 'url', 'published_at','category','image','source']

from .models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('user', 'interests')