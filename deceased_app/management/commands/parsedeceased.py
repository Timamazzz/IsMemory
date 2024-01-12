import base64
import imghdr

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

            for i in range(1, 2):
                url = f'https://memorial31.ru/graves/search/results?surName=&name=&middleName=&yearOfBirth=&birth-status=exactly&yearOfDeath=3000&death-status=after&locality=&graveyard=Ячнево&page={i}'
                page = requests.get(url, headers=headers)
                soup = BeautifulSoup(page.text, 'html.parser')

                items = soup.find_all('a', class_='new-search-results-item')
                for item in items:
                    deceased_url = item['href']
                    deceased_response = requests.get(deceased_url, headers=headers)
                    soup = BeautifulSoup(deceased_response.text, 'html.parser')
                    deceased_right_div = soup.find('div', class_='deceased-right')

                    if deceased_right_div:
                        fio = deceased_right_div.find('h1').text.strip()
                        dob = soup.find('h6', text='Дата рождения').find_next('p').text.strip()
                        dod = soup.find('h6', text='Дата смерти').find_next('p').text.strip()

                        deceased = Deceased.objects.create(
                            first_name=fio.split()[0] if len(fio.split()) > 0 else None,
                            last_name=fio.split()[2] if len(fio.split()) > 2 else None,
                            patronymic=fio.split()[1] if len(fio.split()) > 1 else None,
                            birth_date=dob,
                            death_date=dod
                        )

                        if deceased:
                            coordinates_str = soup.find('h6', text='Место захоронения').find_next('p').text.strip()
                            coordinates = [float(coord.strip()) for coord in coordinates_str.split(',')]

                            coordinates_array = [
                                [coordinates[0] + 0.000009, coordinates[1] + 0.000009],
                                [coordinates[0] + 0.000009, coordinates[1] - 0.000009],
                                [coordinates[0] - 0.000009, coordinates[1] - 0.000009],
                                [coordinates[0] - 0.000009, coordinates[1] + 0.000009],
                                [coordinates[0] + 0.000009, coordinates[1] + 0.000009]
                            ]

                            cemetery_plot = CemeteryPlot.objects.create(
                                cemetery=cemetery,
                                coordinates=coordinates_array,
                                type=CemeteryPlotTypeEnum.BURIAL.name,
                                status=CemeteryPlotStatusEnum.OCCUPIED.name
                            )

                            if cemetery_plot:
                                deceased.cemetery_plot = cemetery_plot
                                deceased.save()

                                image_items = soup.select('.deceased-gallery-item img')
                                image_urls = [item['src'] for item in image_items]

                                for image_url in image_urls:
                                    parts = image_url.split(',')
                                    image_data = parts[1]
                                    decoded_data = base64.b64decode(image_data)
                                    image_format = imghdr.what(None, h=decoded_data)

                                    cemetery_plot_image = CemeteryPlotImage.objects.create(
                                        cemetery_plot=cemetery_plot,
                                        file=image_url,
                                        original_name=f'after_parse_image.{image_format}'
                                    )

            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f'Total execution time: {elapsed_time} seconds')

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An error occurred: {e}'))
