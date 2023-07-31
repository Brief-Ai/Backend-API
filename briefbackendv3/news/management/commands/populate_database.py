import requests
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from news.models import Article

class Command(BaseCommand):
    help = 'Fetches latest news articles from mediastack API and saves them to the database'

    def handle(self, *args, **options):
        api_key = 'f11cf661ab144dcd5295c1261835846c'
        start_date = datetime.now() - timedelta(days=300)
        end_date = datetime.now()
        params = {
            'access_key': api_key,
            'languages': 'en',
            'sort': 'published_desc',
            'limit': 100,
            'offset': 0,
            'date_from': start_date.strftime('%Y-%m-%d'),
            'date_to': end_date.strftime('%Y-%m-%d'),
        }
        total_results = 0
        while True:
            response = requests.get('http://api.mediastack.com/v1/news', params=params)
            data = response.json()
            if 'data' not in data:
                break
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
            total_results += len(data['data'])
            params['offset'] += 100
            if total_results >= 1000:
                break