import random
import time
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from news.models import Article

class Command(BaseCommand):
    help = 'Fetches latest news articles from mediastack API and saves them to the database'

    def handle(self, *args, **options):
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

                params = {
                    'access_key': api_key,
                    'languages': 'en',
                    'sort': 'published_desc',
                    'limit': 100,
                    'offset': 0,
                    'date_from': random_date.strftime('%Y-%m-%d'),
                    'date_to': (random_date + timedelta(days=1)).strftime('%Y-%m-%d'),
                }

                url = 'http://api.mediastack.com/v1/news?' + '&'.join([f'{k}={v}' for k, v in params.items()])
                print(url)

                # Rest of your code for API calls and processing

                # Add a delay between API calls to spread them out
                time.sleep(10)  # Adjust the delay time as needed

# ...
