import sqlite3
from django.shortcuts import render
from rest_framework import generics, filters
from langchain.chat_models import ChatOpenAI
from .models import Search
from .serializers import SearchSerializer
from news.models import Article
from news.serializers import ArticleSerializer

llm = ChatOpenAI(temperature=0.9, openai_api_key='YOUR_API_KEY')



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
        # Add backer user
        search = Search(query=query)
        search.save()
        return self.list(request, *args, **kwargs)

class NewsArticleSearchView(generics.ListAPIView):
    serializer_class = ArticleSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        query = self.request.query_params.get('q')
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM news_article WHERE title LIKE ?", ('%' + query + '%',))
        rows = cursor.fetchall()
        queryset = []
        for row in rows:
            article = Article.objects.get(id=row[0])
            queryset.append(article)
        Search.objects.create(query=query)
        return queryset