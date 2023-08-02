# views.py
from django.shortcuts import render
from rest_framework import generics, filters
from news.models import Article, Search
from news.serializers import ArticleSerializer, SearchSerializer
from langchain.document_loaders import SQLiteLoader
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains import RetrievalQAWithSourcesChain
from dotenv import load_dotenv
import os

load_dotenv()

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

    def get_queryset(self):
        # Load the SQLite database
        db_path = os.path.join(os.getcwd(), 'db.sqlite3')
        loader = SQLiteLoader(db_path)
        db = loader.load()

        # Create an OpenAI object and a Chroma chain
        openai = OpenAIEmbeddings()
        chroma = Chroma(db, openai, verbose=True)
        chain = RetrievalQAWithSourcesChain(chroma, openai, verbose=True)

        # Use the chain to query the database and get the articles
        query = self.request.query_params.get('q')
        results = chain.run(query)

        # Get the articles from the results
        article_ids = [result['source'] for result in results]
        queryset = Article.objects.filter(id__in=article_ids)

        return queryset