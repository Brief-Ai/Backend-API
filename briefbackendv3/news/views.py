from django.shortcuts import render

# Create your views here.
# views.py
from rest_framework import generics, filters

from .models import Search
from .serializers import SearchSerializer
from rest_framework.permissions import IsAuthenticated
from news.models import Article, Search
from news.serializers import ArticleSerializer

class SearchView(generics.ListAPIView):
    queryset = Search.objects.all()
    serializer_class = SearchSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['query']


    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset

    def post(self, request, *args, **kwargs):
        query = request.data.get('query')
        search = Search(user=request.user, query=query)
        search.save()
        return self.list(request, *args, **kwargs)

class NewsArticleSearchView(generics.ListAPIView):
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Article.objects.all()
        query = self.request.query_params.get('q')
        if query:
            queryset = queryset.filter(title__icontains=query) | queryset.filter(description__icontains=query)
        Search.objects.create(user=self.request.user, query=query)
        return queryset