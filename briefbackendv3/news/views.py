# Auth
from rest_framework.decorators import api_view, authentication_classes
from rest_framework_simplejwt.authentication import JWTAuthentication

from django.shortcuts import render
from rest_framework import generics, filters
from langchain.chat_models import ChatOpenAI
from langchain_experimental.sql import SQLDatabaseChain
from langchain.utilities import SQLDatabase
import os
import sqlite3


from fuzzywuzzy import fuzz
from nltk.tokenize import word_tokenize
import nltk


import re
from langchain.prompts import PromptTemplate

from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from langchain.llms.openai import OpenAI
from langchain.agents import AgentExecutor
from langchain.agents.agent_types import AgentType
from langchain.chat_models import ChatOpenAI

import sqlite3

from .models import Search
from .serializers import SearchSerializer
from news.models import Article
from news.serializers import ArticleSerializer

llm = ChatOpenAI(temperature=0.9, openai_api_key='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')
# db = 'db.sqlite3'
db = SQLDatabase.from_uri("sqlite:///db.sqlite3")
os.environ['OPENAI_API_KEY'] = "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"

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
        search = Search(user= self.request.user, query=query)
        search.save()
        return self.list(request, *args, **kwargs)
    

from operator import itemgetter
from django.db.models import Q
@authentication_classes([JWTAuthentication])
class NewsArticleSearchView(generics.ListAPIView):
    serializer_class = ArticleSerializer

    def get_queryset(self):
        query = self.request.query_params.get('q')
        tokens = word_tokenize(query)
        
        # Remove stopwords and non-alphanumeric characters
        keywords = [token.lower() for token in tokens if token.isalnum() and token.lower() not in nltk.corpus.stopwords.words('english')]

    
        q_objects = Q()
        for keyword in keywords:
            q_objects |= Q(title__icontains=keyword) | Q(description__icontains=keyword)
    
        articles = Article.objects.filter(q_objects)
        query = self.request.query_params.get('q')
        results = []
        for article in articles:
            title_score = fuzz.token_set_ratio(word_tokenize(query), word_tokenize(article.title))
            description_score = fuzz.token_set_ratio(word_tokenize(query), word_tokenize(article.description))
            score = title_score + description_score
            results.append((article, score))
        results = sorted(results, key=itemgetter(1))
        Search.objects.create(user_id=2,query=query)
        return [article for article, score in results]