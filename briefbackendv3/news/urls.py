from django.urls import path
from .views import NewsArticleSearchView
from .views import NewsArticleRecommendedView
from .views import UpdateInterests


urlpatterns = [
    path('search/', NewsArticleSearchView.as_view(), name='news_article_search'),
    # Add route for recommended articles
    path('recommended/', NewsArticleRecommendedView.as_view(), name='news_article_recommended'),
    path('update-interests/', UpdateInterests.as_view(), name='update_interests'),
]