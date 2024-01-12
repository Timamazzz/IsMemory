from django.core.management.base import BaseCommand
import requests
from bs4 import BeautifulSoup


class Command(BaseCommand):
    help = ''

    def handle(self, *args, **options):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }

            for i in range(1, 3):
                print('Page:', i)
                url = f'https://memorial31.ru/graves/search/results?surName=&name=&middleName=&yearOfBirth=&birth-status=exactly&yearOfDeath=3000&death-status=after&locality=&graveyard=Ячнево&page={i}'

                response = requests.get(url, headers=headers)
                html = response.text
                soup = BeautifulSoup(html, 'html.parser')

                items = soup.find_all('a', class_='new-search-results-item')
                print('items', items)
                for item in items:
                    href = item['href']
                    print('URL:', href)
                    print('\n')

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An error occurred: {e}'))
