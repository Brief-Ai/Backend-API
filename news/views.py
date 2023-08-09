# Auth
from rest_framework.decorators import api_view, authentication_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from .models import UserProfile
from .serializers import UserProfileSerializer

from django.shortcuts import render
from rest_framework import generics, filters
from langchain.chat_models import ChatOpenAI
from langchain_experimental.sql import SQLDatabaseChain
from langchain.utilities import SQLDatabase
import os
import sqlite3
import ast


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

llm = ChatOpenAI(temperature=0.9, openai_api_key=os.getenv('OPENAPI_KEY'))
# db = 'db.sqlite3'
db = SQLDatabase.from_uri("sqlite:///db.sqlite3")
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAPI_KEY')

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
        search = Search(user=self.request.user, query=query)
        search.save()
        return self.list(request, *args, **kwargs)
    

from operator import itemgetter
from django.db.models import Q
@authentication_classes([JWTAuthentication])
class NewsArticleSearchView(generics.ListAPIView):
    serializer_class = ArticleSerializer


    def extract_keywords(self, query):
        llm = OpenAI(temperature=0, verbose=True)

        template = """
        Summarize the search keywords in exact 1 word or phrase based on the following search query:
        EXAMPLES:
        search query: Tell me some basketball news
        keywords: basketball
        =================================================================
        search query: {history}
        keywords: 
        """
        prompt_template = PromptTemplate(
            input_variables=['history'],
            template=template
        )

        model = OpenAI(temperature=0, model_name="gpt-3.5-turbo")
        in_text = prompt_template.format(history=query)

        interests = model(in_text)
        return interests

    def get_queryset(self):
        query = self.request.query_params.get('q')
        keywords = self.extract_keywords(query)

        q_objects = Q()
        for keyword in keywords:
            q_objects |= Q(title__icontains=keyword)
            # You can also search in description if needed
            # q_objects |= Q(description__icontains=keyword)

        articles = Article.objects.filter(q_objects)
        results = []
        for article in articles:
            title_score = fuzz.token_set_ratio(word_tokenize(query), word_tokenize(article.title))
            # description_score = fuzz.token_set_ratio(word_tokenize(query), word_tokenize(article.description))
            # + description_score
            score = title_score 
            results.append((article, score))
        results = sorted(results, key=itemgetter(1), reverse=True)
        Search.objects.create(user_id=self.request.user.id, query=query)
        return [article for article, score in results]
@authentication_classes([JWTAuthentication])
class UpdateInterests(generics.ListAPIView):
    def post(self, request):
        user_profile, created = UserProfile.objects.get_or_create(user_id=self.request.user.id)
        
        interests = request.data.get('interests', [])

        user_profile.interests = interests
        user_profile.save()

        return Response({"interests": interests})

@authentication_classes([JWTAuthentication])
class GetInterests(generics.ListAPIView):
    def get(self, request):
        try:
            user_profile = UserProfile.objects.get(user_id=self.request.user.id)
            interests = user_profile.interests
            return Response({'interests': interests}, status=status.HTTP_200_OK)
        except UserProfile.DoesNotExist:
            return Response({'message': 'User profile not found'}, status=status.HTTP_404_NOT_FOUND)

# ... (previous imports)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import numpy as np
import sqlite3
from numpy.linalg import norm
from nltk.tokenize import word_tokenize

class InterestBasedArticleView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            user_profile = UserProfile.objects.get(user_id=self.request.user.id)
            imported_interests = user_profile.interests
        except UserProfile.DoesNotExist:
            return Response({'message': 'User profile not found'}, status=status.HTTP_404_NOT_FOUND)
        if not imported_interests:
            return Response({'message': 'No interests available'}, status=status.HTTP_400_BAD_REQUEST)

        # Convert str type from database into functional list
        # Convert by splitting string by comma but dont include [ and ] and dont include existing quotes
        interests_list = imported_interests[1:-1].split(', ') 
        user_interests = [item.strip("'") for item in interests_list]

        # # Debug, print user interests
        # user_interests = ['writing', 'anime', 'art']
        print('User interests: ', user_interests)
        print('User interests type: ', type(user_interests))
    
        def load_glove_embeddings(file_path):
            embeddings_dict = {}
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    values = line.split()
                    word = values[0]
                    embedding = [float(val) for val in values[1:]]
                    embeddings_dict[word] = embedding
            return embeddings_dict

        # Load embeddings and calculate interest vector
        glove_file_path = 'glove.6B.50d.txt'
        embeddings_dict = load_glove_embeddings(glove_file_path)

        interest_vector = None
        count = 0
        for interest in user_interests:
            interest = interest.lower()
            if interest in embeddings_dict:
                if interest_vector is None:
                    interest_vector = np.array(embeddings_dict[interest])
                else:
                    interest_vector += np.array(embeddings_dict[interest])
                count += 1
        if count > 0:
            interest_vector /= count

        # Calculate similarity and retrieve relevant articles
        data = Article.objects.values('title', 'description')

        data = [each['title'] + each['description'] for each in data]

        sent_embedding = []
        for i in range(len(data)):
            sent = word_tokenize(data[i])

            temp = None
            count = 0
            for each in sent:
                each = each.lower()
                if each in embeddings_dict:
                    if temp is None:
                        temp = np.array(embeddings_dict[each])
                    else:
                        temp += np.array(embeddings_dict[each])
                    count += 1

            temp = temp / count
            sent_embedding.append(temp)

        result = []
        for idx, val in enumerate(data):
            doc_vector = sent_embedding[idx]
            similarity = np.sum(interest_vector * doc_vector) / (norm(interest_vector) * norm(doc_vector))
            result.append((idx + 1, similarity))

        result = sorted(result, key=lambda x: x[1], reverse=True)

        relevant_article_ids = [idx[0] for idx in result[:8]]
        
        # Retrieve relevant articles from the database
        relevant_articles = Article.objects.filter(id__in=relevant_article_ids)
        serializer = ArticleSerializer(relevant_articles, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)