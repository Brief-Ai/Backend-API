from django.urls import path
from .views import NewsArticleSearchView

urlpatterns = [
    path('search/', NewsArticleSearchView.as_view(), name='news_article_search'),
]