import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

total_pages = 3117
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/91.0.4472.124 Safari/537.36'
}

for page_num in tqdm(range(1, total_pages + 1), desc='Pages processed'):
    url = (f'https://memorial31.ru/graves/search/results?surName=&name=&middleName=&yearOfBirth=&birth'
           f'-status=exactly&yearOfDeath=3000&death-status=after&locality=&graveyard=Ячнев'
           f'о&page={page_num}')
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.text, 'html.parser')

    items = soup.find_all('a', class_='new-search-results-item')

    print('items count', len(items))
