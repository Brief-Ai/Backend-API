import os
import time
from datetime import datetime, timedelta
import requests
from django.core.management.base import BaseCommand
from news.models import Article  # Replace 'your_app' with your actual app name
from django.db import models  # Import the models module

class Command(BaseCommand):
    help = 'Fetch articles from the MediaStack API'

    def handle(self, *args, **options):
        api_key = os.getenv('MEDIASTACK_API_KEY')  # Fetch API key from environment variable
        articles_to_fetch = 300
        fetched_articles = 0
        end_date = datetime.now()

        max_article_id = Article.objects.aggregate(max_id=models.Max('id'))['max_id'] or 0

        while fetched_articles < articles_to_fetch:
            start_date = end_date - timedelta(days=30)

            while start_date <= end_date and fetched_articles < articles_to_fetch:
                params = {
                    'access_key': api_key,
                    'languages': 'en',
                    'sort': 'published_desc',
                    'limit': min(100, articles_to_fetch - fetched_articles),
                    'offset': 0,  # Reset offset for each day
                    'date_from': start_date.strftime('%Y-%m-%d'),
                    'date_to': end_date.strftime('%Y-%m-%d'),  # Use end_date here
                }

                print(f"Fetching articles from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
                # Define url 
                
                response = requests.get('http://api.mediastack.com/v1/news', params=params)
                
                data = response.json()
                if 'data' not in data:
                    print("No data found in API response.")
                    break
                for article in data['data']:
                    if not Article.objects.filter(url=article['url']).exists():
                        max_article_id += 1
                        Article.objects.create(
                            id=max_article_id,
                            title=article['title'],
                            description=article['description'],
                            url=article['url'],
                            published_at=datetime.fromisoformat(article['published_at']),
                            language=article['language'],
                            image=article['image'],
                            source=article['source'],
                        )
                        fetched_articles += 1
                        # print(f"Fetched article: {article['title']}")
                        # Added Article
                        print(f"ADDED article: {article['title']}")
                    else:
                        print(f"Article already exists: {article['title']}")
                params['offset'] += 100

                # Add a delay between API calls to spread them out
                time.sleep(10)  # Adjust the delay time as needed

                start_date += timedelta(days=1)

            end_date -= timedelta(days=30)
