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
    

@authentication_classes([JWTAuthentication])
class NewsArticleSearchView(generics.ListAPIView):
    serializer_class = ArticleSerializer

    def get_queryset(self):
        query = self.request.query_params.get('q')
        print(query)
        # db_chain = SQLDatabaseChain(llm=llm, database=db, verbose=True)
        toolkit = SQLDatabaseToolkit(db=db, llm=llm)
        agent_executor = create_sql_agent(
            llm=llm,
            toolkit=toolkit,
            verbose=True,
            agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        )
        # query = query.split()
        # query = " or ".join(query)
        template = """
            Summarize the keywords from the search query:
            EXAMPLES:
            query: What happened in NBA recently
            keywords: NBA
            ================================================================
            query: {query}
            keywords:
            """
        prompt_template = PromptTemplate(
            input_variables=['query'],
            template=template
        )
        model = OpenAI(temperature=0, model_name="gpt-3.5-turbo")
        in_text = prompt_template.format(query=query)
        
        query = model(in_text)
        
        ids = agent_executor.run(f"Return ONLY the ID for records whose description content or title content is roughly about {query}, reorder the results by how relevant it is to {query} . Return all results")
        
        # ids = db_chain.run(f"return only the id for records whose descriptions or titles are about {query} in the news_article table. each record should be separated by a space.")
        #write a query that returns the id for records whose description content or title content is roughly about {query} or reoder the results by the most relevant to {query} in the news_article table. each record should be separated by a space. no limit. 
        # ids = db_chain.run(f"return the id for records whose description content or title content is roughly about {query}, reorder the results by the most relevant to {query}, change order of how {query} is stated if it can make the search more accurate, in the news_article table. each record should be separated by a space. no limit.")
        # ids = db_chain.run(f"return the id for records whose description content or title content is roughly about {query}, reorder the results by the most relevant to {query}, change order of how {query} is stated if it can make the search more accurate. In the news_article table. each record separated by space. no limit.")
        
        # conn = sqlite3.connect('sqlite3.db')
        # cursor = conn.cursor()
        ids_list = re.findall(r'\d+', ids)
        queryset=[]
        for l_id in ids_list:
            article = Article.objects.get(id=l_id)
            queryset.append(article)
        Search.objects.create(user_id=self.request.user.id,query=query)
        return queryset