from django.urls import path
from .views import NewsArticleSearchView
from .views import NewsArticleRecommendedView

urlpatterns = [
    path('search/', NewsArticleSearchView.as_view(), name='news_article_search'),
    
    # Add route for recommended articles
    path('recommended/', NewsArticleRecommendedView.as_view(), name='news_article_recommended'),
]