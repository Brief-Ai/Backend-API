from django.shortcuts import render
from rest_framework import generics, filters
from langchain import ChatOpenAI
from langchain import SQLDatabaseChain
import sqlite3

from .models import Search
from .serializers import SearchSerializer
from news.models import Article
from news.serializers import ArticleSerializer

llm = ChatOpenAI(temperature=0.9, openai_api_key='YOUR_API_KEY')
db = 'db.sqlite3'

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
        db_chain = SQLDatabaseChain(llm=llm, database=db, verbose=True)
        ids = db_chain.run(f"return only the id for records that are about {query} in the news_articles table. each record should be separated by a space.")
        conn = sqlite3.connect('your_database_file.db')
        cursor = conn.cursor()
        ids_list = ids.split()
        queryset=[]
        for l_id in ids_list:
            article = Article.objects.get(id=l_id)
            queryset.append(article)
        Search.objects.create(query=query)
        return queryset