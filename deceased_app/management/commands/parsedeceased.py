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


def format_date(date_str):
    if not date_str:
        return None
    parts = date_str.split('.')
    year = parts[2].zfill(4)
    month = parts[1].zfill(2)
    day = parts[0].zfill(2)
    return f"{year}-{month}-{day}"


# Остальные импорты...

# Остальные импорты...

class Command(BaseCommand):
    help = ''

    def handle(self, *args, **options):
        try:
            cemetery = Cemetery.objects.get(name='Ячнево')

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/91.0.4472.124 Safari/537.36'
            }
            total_pages = 3117
            loaded_deceased = 0
            loaded_plots = 0
            loaded_images = 0

            # for page_num in tqdm(range(1, total_pages + 1), desc='Pages processed'):
            url = (f'https://memorial31.ru/graves/search/results?surName=&name=&middleName=&yearOfBirth=&birth'
                   f'-status=exactly&yearOfDeath=3000&death-status=after&locality=&graveyard=Ячнев'
                   f'о&page={102}')
            page = requests.get(url, headers=headers)
            soup_main = BeautifulSoup(page.text, 'html.parser')
            deceased_objects = []
            plot_objects = []
            plot_images = []
            items = soup_main.find_all('a', class_='new-search-results-item')
            for item_num, item in enumerate(items, start=1):
                deceased_url = item['href']
                deceased_response = requests.get(deceased_url, headers=headers)
                soup_deceased = BeautifulSoup(deceased_response.text, 'html.parser')
                deceased_right_div = soup_deceased.find('div', class_='deceased-right')

                if deceased_right_div:
                    fio = deceased_right_div.find('h1').text.strip()
                    dob = soup_deceased.find('h6', text='Дата рождения').find_next('p').text.strip()
                    dod = soup_deceased.find('h6', text='Дата смерти').find_next('p').text.strip()

                    dob_formatted = format_date(dob)
                    dod_formatted = format_date(dod)

                    deceased = Deceased(
                        first_name=fio.split()[0] if len(fio.split()) > 0 else None,
                        last_name=fio.split()[2] if len(fio.split()) > 2 else None,
                        patronymic=fio.split()[1] if len(fio.split()) > 1 else None,
                        birth_date=dob_formatted,
                        death_date=dod_formatted
                    )
                    deceased_objects.append(deceased)

                    coordinates_str = soup_deceased.find('h6', text='Место захоронения').find_next('p').text.strip()
                    if coordinates_str:
                        coordinates = [float(coord.strip()) for coord in coordinates_str.split(',')]
                        coordinates_array = [
                            [
                                [coordinates[0] + 0.000009, coordinates[1] + 0.000009],
                                [coordinates[0] + 0.000009, coordinates[1] - 0.000009],
                                [coordinates[0] - 0.000009, coordinates[1] - 0.000009],
                                [coordinates[0] - 0.000009, coordinates[1] + 0.000009],
                                [coordinates[0] + 0.000009, coordinates[1] + 0.000009]
                            ]
                        ]
                        plot = CemeteryPlot(
                            cemetery=cemetery,
                            coordinates=coordinates_array,
                            type=CemeteryPlotTypeEnum.BURIAL.name,
                            status=CemeteryPlotStatusEnum.OCCUPIED.name
                        )
                        plot_objects.append(plot)

                        image_items = soup_deceased.select('.deceased-gallery-item img')
                        image_urls = [item['src'] for item in image_items]

                        for image_url in image_urls:
                            parts = image_url.split(',')
                            image_data = parts[1]
                            decoded_data = base64.b64decode(image_data)
                            image_format = imghdr.what(None, h=decoded_data)
                            file_name = f'cemetery_plot_{plot.id}.{image_format}'

                            if not default_storage.exists(file_name):
                                img = Image.open(io.BytesIO(decoded_data))
                                max_size = (800, 600)
                                img.thumbnail(max_size, Image.Resampling.LANCZOS)

                                output_buffer = io.BytesIO()
                                img.save(output_buffer, optimize=True, quality=95, format=image_format)
                                output_buffer.seek(0)
                                compressed_data = output_buffer.getvalue()

                                file_path = default_storage.save(file_name, ContentFile(compressed_data))

                                plot_image = CemeteryPlotImage(
                                    cemetery_plot=plot,
                                    file=file_path,
                                    original_name=file_name
                                )
                                plot_images.append(plot_image)

            self.stdout.write(self.style.SUCCESS(f'deceased_objects: {deceased_objects}'))
            created_deceased = Deceased.objects.bulk_create(deceased_objects)
            loaded_deceased += len(created_deceased)

            self.stdout.write(self.style.SUCCESS(f'plot_objects: {plot_objects}'))
            created_plots = CemeteryPlot.objects.bulk_create(plot_objects)
            loaded_plots += len(created_plots)

            for plot, deceased in zip(created_plots, created_deceased):
                deceased.cemetery_plot = plot
                deceased.save()

            self.stdout.write(self.style.SUCCESS(f'plot_images: {plot_images}'))
            CemeteryPlotImage.objects.bulk_create(plot_images)
            loaded_images += len(plot_images)

            self.stdout.write(self.style.SUCCESS(f'Total loaded deceased: {loaded_deceased}'))
            self.stdout.write(self.style.SUCCESS(f'Total loaded plots: {loaded_plots}'))
            self.stdout.write(self.style.SUCCESS(f'Total loaded images: {loaded_images}'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An error occurred: {e}'))

