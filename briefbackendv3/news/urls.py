from django.urls import path
from .views import NewsArticleSearchView
from .views import InterestBasedArticleView
from .views import UpdateInterests
from .views import GetInterests


urlpatterns = [
    path('search/', NewsArticleSearchView.as_view(), name='news_article_search'),
    # Add route for recommended articles
    path('recommended/', InterestBasedArticleView.as_view(), name='interest_based_article'),
    path('update-interests/', UpdateInterests.as_view(), name='update_interests'),
    path('get-interests/', GetInterests.as_view(), name='get-interests'),
]