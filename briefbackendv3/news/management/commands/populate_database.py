<<<<<<< HEAD
import requests
=======
import random
>>>>>>> 2906d76e9cd7b1f8edf2b92cd05bb09a8a2b88ba
import time
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from news.models import Article

class Command(BaseCommand):
    help = 'Fetches and adds 3000 latest news articles from mediastack API to the database'

    def handle(self, *args, **options):
<<<<<<< HEAD
        api_key = 'cf16d9738a9525f1525c1667848c7391'
        articles_to_fetch = 3000
        fetched_articles = 0
        end_date = datetime.now()

        while fetched_articles < articles_to_fetch:
            start_date = end_date - timedelta(days=30)

            while start_date <= end_date and fetched_articles < articles_to_fetch:
=======
        api_key = 'xxx'

        for month_offset in range(10):
            end_date = datetime.now() - timedelta(days=30 * month_offset)
            start_date = end_date - timedelta(days=30)

            print(f"Date Range: {start_date.strftime('%Y-%m-%d')} - {end_date.strftime('%Y-%m-%d')}")

            for _ in range(10):
                random_day = random.randint(1, 30)
                random_date = start_date + timedelta(days=random_day)

                # Calculate an offset in hours for more data variety
                offset_hours = random.randint(0, 23)
                random_date += timedelta(hours=offset_hours)

>>>>>>> 2906d76e9cd7b1f8edf2b92cd05bb09a8a2b88ba
                params = {
                    'access_key': api_key,
                    'languages': 'en',
                    'sort': 'published_desc',
<<<<<<< HEAD
                    'limit': min(100, articles_to_fetch - fetched_articles),
                    'offset': 0,
                    'date_from': start_date.strftime('%Y-%m-%d'),
                    'date_to': start_date.strftime('%Y-%m-%d'),
                }

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
                        language=article['language'],
                        image=article['image'],
                        source=article['source'],
                    )
                    fetched_articles += 1
                params['offset'] += 100
=======
                    'limit': 100,
                    'offset': 0,
                    'date_from': random_date.strftime('%Y-%m-%d'),
                    'date_to': (random_date + timedelta(days=1)).strftime('%Y-%m-%d'),
                }

                url = 'http://api.mediastack.com/v1/news?' + '&'.join([f'{k}={v}' for k, v in params.items()])
                print(url)

                # Rest of your code for API calls and processing
>>>>>>> 2906d76e9cd7b1f8edf2b92cd05bb09a8a2b88ba

                # Add a delay between API calls to spread them out
                time.sleep(10)  # Adjust the delay time as needed

<<<<<<< HEAD
                start_date += timedelta(days=1)

            end_date -= timedelta(days=30)
=======
# ...
>>>>>>> 2906d76e9cd7b1f8edf2b92cd05bb09a8a2b88ba
