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


class Command(BaseCommand):
    help = ''

    def handle(self, *args, **options):
        try:
            cemetery = Cemetery.objects.get(pk=8)
            start_time = time.time()
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            total_pages = 1
            loaded_deceased = 0
            loaded_plots = 0
            for page_num in range(1, total_pages + 1):
                self.stdout.write(
                    self.style.SUCCESS(f'Processing page {(page_num / total_pages) * 100:.0f}%'),
                    ending='\r'
                )
                self.stdout.flush()
                url = f'https://memorial31.ru/graves/search/results?surName=&name=&middleName=&yearOfBirth=&birth-status=exactly&yearOfDeath=3000&death-status=after&locality=&graveyard=Ячнево&page={page_num}'
                page = requests.get(url, headers=headers)
                soup = BeautifulSoup(page.text, 'html.parser')

                items = soup.find_all('a', class_='new-search-results-item')
                total_items = len(items)
                for item_num, item in enumerate(items, start=1):
                    self.stdout.write(
                        self.style.SUCCESS(f'Processing item {(item_num / total_items) * 100:.0f}%'),
                        ending='\r'
                    )
                    self.stdout.flush()
                    deceased_url = item['href']
                    deceased_response = requests.get(deceased_url, headers=headers)
                    soup = BeautifulSoup(deceased_response.text, 'html.parser')
                    deceased_right_div = soup.find('div', class_='deceased-right')

                    if deceased_right_div:
                        fio = deceased_right_div.find('h1').text.strip()
                        dob = soup.find('h6', text='Дата рождения').find_next('p').text.strip()
                        dod = soup.find('h6', text='Дата смерти').find_next('p').text.strip()

                        dob_formatted = datetime.strptime(dob, "%d.%m.%Y").strftime("%Y-%m-%d") if dob else None
                        dod_formatted = datetime.strptime(dod, "%d.%m.%Y").strftime("%Y-%m-%d") if dod else None

                        deceased = Deceased.objects.create(
                            first_name=fio.split()[0] if len(fio.split()) > 0 else None,
                            last_name=fio.split()[2] if len(fio.split()) > 2 else None,
                            patronymic=fio.split()[1] if len(fio.split()) > 1 else None,
                            birth_date=dob_formatted,
                            death_date=dod_formatted
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

                            cemetery_plot = CemeteryPlot.objects.create(
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

                                    file_name = f'after_parse_image_{datetime.now().strftime("%Y%m%d%H%M%S")}.{image_format}'
                                    file_path = default_storage.save(file_name, ContentFile(decoded_data))

                                    cemetery_plot_image = CemeteryPlotImage.objects.create(
                                        land_plot=cemetery_plot,
                                        file=file_path,
                                        original_name=file_name
                                    )

            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f'Total execution time: {elapsed_time} seconds')
            print(f'Total loaded deceased: {loaded_deceased}')
            print(f'Total loaded plots: {loaded_plots}')

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An error occurred: {e}'))
