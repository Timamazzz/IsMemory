import base64
import imghdr
from datetime import datetime

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.management.base import BaseCommand
import requests
from bs4 import BeautifulSoup
import time

from deceased_app.models import Deceased
from docs_app.models import CemeteryPlotImage
from locations_app.enums import CemeteryPlotTypeEnum, CemeteryPlotStatusEnum
from locations_app.models import Cemetery, CemeteryPlot
from tqdm import tqdm
from PIL import Image
import io


class Command(BaseCommand):
    help = ''

    def handle(self, *args, **options):
        cemetery = Cemetery.objects.get(name='Ячнево')

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/91.0.4472.124 Safari/537.36'
        }
        total_pages = 3117
        loaded_deceased = 0
        loaded_plots = 0
        # for page_num in tqdm(range(1, total_pages + 1), desc='Pages processed'):
        url = (f'https://memorial31.ru/graves/search/results?surName=&name=&middleName=&yearOfBirth=&birth'
               f'-status=exactly&yearOfDeath=3000&death-status=after&locality=&graveyard=Ячнев'
               f'о&page={81}')
        page = requests.get(url, headers=headers)
        soup = BeautifulSoup(page.text, 'html.parser')

        items = soup.find_all('a', class_='new-search-results-item')
        for item_num, item in enumerate(items, start=1):
            deceased_url = item['href']
            deceased_response = requests.get(deceased_url, headers=headers)
            soup = BeautifulSoup(deceased_response.text, 'html.parser')
            deceased_right_div = soup.find('div', class_='deceased-right')

            if deceased_right_div:
                fio = deceased_right_div.find('h1').text.strip()
                dob = soup.find('h6', text='Дата рождения').find_next('p').text.strip()
                dod = soup.find('h6', text='Дата смерти').find_next('p').text.strip()

                self.stdout.write(self.style.SUCCESS(f'dob:{dob} dod:{dod}'))

                try:
                    dob_formatted = datetime.strptime(dob, "%d.%m.%Y").strftime("%Y-%m-%d") if dob else None
                except ValueError as e:
                    dob_formatted = None

                try:
                    dod_formatted = datetime.strptime(dod, "%d.%m.%Y").strftime("%Y-%m-%d") if dod else None
                except ValueError as e:
                    dod_formatted = None

                self.stdout.write(self.style.SUCCESS(f'dob_formatted:{dob_formatted} dod:{dod_formatted}'))

                try:
                    deceased, created = Deceased.objects.get_or_create(
                        first_name=fio.split()[0] if len(fio.split()) > 0 else None,
                        last_name=fio.split()[2] if len(fio.split()) > 2 else None,
                        patronymic=fio.split()[1] if len(fio.split()) > 1 else None,
                        birth_date=dob_formatted,
                        death_date=dod_formatted
                    )
                except ValueError as e:
                    deceased, created = Deceased.objects.get_or_create(
                        first_name=fio.split()[0] if len(fio.split()) > 0 else None,
                        last_name=fio.split()[2] if len(fio.split()) > 2 else None,
                        patronymic=fio.split()[1] if len(fio.split()) > 1 else None,
                    )

                if deceased:
                    loaded_deceased += 1
                    coordinates_str = soup.find('h6', text='Место захоронения').find_next('p').text.strip()
                    coordinates = [float(coord.strip()) for coord in coordinates_str.split(',')]

                    coordinates_array = [[
                        [coordinates[0] + 0.000009, coordinates[1] + 0.000009],
                        [coordinates[0] + 0.000009, coordinates[1] - 0.000009],
                        [coordinates[0] - 0.000009, coordinates[1] - 0.000009],
                        [coordinates[0] - 0.000009, coordinates[1] + 0.000009],
                        [coordinates[0] + 0.000009, coordinates[1] + 0.000009]
                    ]]

                    cemetery_plot, created = CemeteryPlot.objects.get_or_create(
                        cemetery=cemetery,
                        coordinates=coordinates_array,
                        type=CemeteryPlotTypeEnum.BURIAL.name,
                        status=CemeteryPlotStatusEnum.OCCUPIED.name
                    )

                    if cemetery_plot:
                        loaded_plots += 1
                        deceased.cemetery_plot = cemetery_plot
                        deceased.save()

                        image_items = soup.select('.deceased-gallery-item img')
                        image_urls = [item['src'] for item in image_items]

                        for image_url in image_urls:
                            parts = image_url.split(',')
                            image_data = parts[1]
                            decoded_data = base64.b64decode(image_data)
                            image_format = imghdr.what(None, h=decoded_data)

                            img = Image.open(io.BytesIO(decoded_data))

                            max_size = (800, 600)

                            img.thumbnail(max_size, Image.Resampling.LANCZOS)

                            output_buffer = io.BytesIO()
                            img.save(output_buffer, optimize=True, quality=95, format=image_format)
                            output_buffer.seek(0)
                            compressed_data = output_buffer.getvalue()

                            file_name = f'after_parse_image_{datetime.now().strftime("%Y%m%d%H%M%S")}.{image_format}'
                            file_path = default_storage.save(file_name, ContentFile(compressed_data))

                            CemeteryPlotImage.objects.get_or_create(
                                cemetery_plot=cemetery_plot,
                                file=file_path,
                                original_name=file_name
                            )

    self.stdout.write(self.style.SUCCESS(f'Total loaded deceased: {loaded_deceased}'))
    self.stdout.write(self.style.SUCCESS(f'Total loaded plots: {loaded_plots}'))

