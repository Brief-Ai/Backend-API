import requests
from datetime import datetime
from django.core.management.base import BaseCommand
from news.models import Article

class Command(BaseCommand):
    help = 'Fetches latest news articles from mediastack API and saves them to the database'

    def handle(self, *args, **options):
        params = {
            'access_key': 'YOUR_ACCESS_KEY',
            'languages': 'en',
            'limit': 10,
        }
        response = requests.get('https://api.mediastack.com/v1/news', params=params)
        data = response.json()
        for article in data['data']:
            Article.objects.create(
                title=article['title'],
                description=article['description'],
                url=article['url'],
                published_at=datetime.fromisoformat(article['published_at']),
                language = article['language'],
                image = article['image'],
                source = article['source'],
            )