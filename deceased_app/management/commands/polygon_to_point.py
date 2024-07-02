from django.core.management.base import BaseCommand
from locations_app.models import CemeteryPlot


class Command(BaseCommand):
    help = 'Convert cemetery plot polygons to points'

    def handle(self, *args, **options):
        try:
            cemetery_plots = CemeteryPlot.objects.all()
            updated_plots = 0

            for plot in cemetery_plots:
                if isinstance(plot.coordinates, list) and len(plot.coordinates) > 0:
                    polygon = plot.coordinates[0]
                    if isinstance(polygon, list) and len(polygon) > 0:
                        first_point = polygon[0]
                        if isinstance(first_point, list) and len(first_point) == 2:
                            lat, lon = first_point
                            new_coordinates = [lat - 0.000009, lon - 0.000009]
                            plot.coordinates = [new_coordinates]
                            plot.save()
                            updated_plots += 1
                            print('plot', plot.id)

            self.stdout.write(self.style.SUCCESS(f'Updated {updated_plots} cemetery plots to points.'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An error occurred: {e}'))
