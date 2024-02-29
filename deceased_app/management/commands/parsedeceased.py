import base64
import imghdr
import io
import uuid

import requests
from bs4 import BeautifulSoup
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.management.base import BaseCommand

from deceased_app.models import Deceased
from docs_app.models import CemeteryPlotImage
from locations_app.enums import CemeteryPlotTypeEnum, CemeteryPlotStatusEnum
from locations_app.models import Cemetery, CemeteryPlot
from tqdm import tqdm
from PIL import Image


def format_date(date_str):
    if not date_str:
        return None
    parts = date_str.split('.')
    year = parts[2].zfill(4)
    month = parts[1].zfill(2)
    day = parts[0].zfill(2)
    return f"{year}-{month}-{day}"


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
            start_page = 1
            loaded_deceased = 0
            loaded_plots = 0
            loaded_images = 0

            for page_num in tqdm(range(start_page, total_pages + 1), desc='Pages processed'):
                url = (f'https://memorial31.ru/graves/search/results?surName=&name=&middleName=&yearOfBirth=&birth'
                       f'-status=exactly&yearOfDeath=3000&death-status=after&locality=&graveyard=Ячнево&page={page_num}')
                page = requests.get(url, headers=headers)
                soup_main = BeautifulSoup(page.text, 'html.parser')

                items = soup_main.find_all('a', class_='new-search-results-item')
                deceased_bulk_list = []
                image_bulk_list = []

                for item_num, item in enumerate(items, start=1):
                    deceased_url = item['href']
                    deceased_response = requests.get(deceased_url, headers=headers)
                    soup_deceased = BeautifulSoup(deceased_response.text, 'html.parser')
                    deceased_right_div = soup_deceased.find('div', class_='deceased-right')

                    if deceased_right_div:
                        fio = deceased_right_div.find('h1').text.strip()
                        fio = deceased_right_div.find('h1').text.strip()
                        dob = soup_deceased.find('h6', text='Дата рождения').find_next('p').text.strip()
                        dod = soup_deceased.find('h6', text='Дата смерти').find_next('p').text.strip()

                        dob_formatted = format_date(dob)
                        dod_formatted = format_date(dod)

                        cemetery_plot_coordinates = None
                        coordinates_str = soup_deceased.find('h6', text='Место захоронения').find_next('p').text.strip()
                        if coordinates_str:
                            coordinates = [float(coord.strip()) for coord in coordinates_str.split(',') if
                                           coord.strip()]

                            if len(coordinates) >= 2:
                                lat, lon = coordinates[:2]
                                cemetery_plot_coordinates = [
                                    [
                                        [lat + 0.000009, lon + 0.000009],
                                        [lat + 0.000009, lon - 0.000009],
                                        [lat - 0.000009, lon - 0.000009],
                                        [lat - 0.000009, lon + 0.000009],
                                        [lat + 0.000009, lon + 0.000009]
                                    ]
                                ]
                        loaded_plots += 1

                        image_items = soup_deceased.select('.deceased-gallery-item img')
                        image_urls = [item['src'] for item in image_items]

                        plot, _ = CemeteryPlot.objects.get_or_create(
                            cemetery=cemetery,
                            coordinates=cemetery_plot_coordinates,
                            type=CemeteryPlotTypeEnum.BURIAL.name,
                            status=CemeteryPlotStatusEnum.OCCUPIED.name
                        )

                        for i, image_url in enumerate(image_urls):
                            parts = image_url.split(',')
                            image_data = parts[1]
                            decoded_data = base64.b64decode(image_data)
                            image_format = imghdr.what(None, h=decoded_data)
                            file_name = f'{uuid.uuid4()}.{image_format}'

                            img = Image.open(io.BytesIO(decoded_data))
                            max_size = (800, 600)
                            img.thumbnail(max_size, Image.Resampling.LANCZOS)

                            output_buffer = io.BytesIO()
                            img.save(output_buffer, optimize=True, quality=95, format=image_format)
                            output_buffer.seek(0)
                            compressed_data = output_buffer.getvalue()

                            file_path = default_storage.save(file_name, ContentFile(compressed_data))

                            if i == 0:
                                plot_image = CemeteryPlotImage(
                                    file=file_path,
                                    original_name=file_name,
                                    cemetery_plot=plot,
                                    is_preview=True
                                )
                            else:
                                plot_image = CemeteryPlotImage(
                                    file=file_path,
                                    original_name=file_name,
                                    cemetery_plot=plot,
                                    is_preview=False
                                )

                            image_bulk_list.append(plot_image)

                        deceased = Deceased(
                            first_name=fio.split()[0] if len(fio.split()) > 0 else None,
                            last_name=fio.split()[2] if len(fio.split()) > 2 else None,
                            patronymic=fio.split()[1] if len(fio.split()) > 1 else None,
                            birth_date=dob_formatted,
                            death_date=dod_formatted,
                            cemetery_plot=plot
                        )

                        deceased_bulk_list.append(deceased)

                Deceased.objects.bulk_create(deceased_bulk_list)
                CemeteryPlotImage.objects.bulk_create(image_bulk_list)

                loaded_deceased += len(deceased_bulk_list)
                loaded_images += len(image_bulk_list)

            self.stdout.write(self.style.SUCCESS(f'deceased loaded: {loaded_deceased}'))
            self.stdout.write(self.style.SUCCESS(f'plot loaded: {loaded_plots}'))
            self.stdout.write(self.style.SUCCESS(f'images loaded: {loaded_images}'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An error occurred: {e}'))
