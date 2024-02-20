from django.core.management.base import BaseCommand
from django.conf import settings
import mysql.connector


class Command(BaseCommand):
    help = 'Creates the database and performs migrations'

    def handle(self, *args, **options):
        db_settings = settings.DATABASES['default']

        try:
            connection = mysql.connector.connect(
                host=db_settings['HOST'],
                user=db_settings['USER'],
                password=db_settings['PASSWORD'],
                charset='utf8mb4'
            )

            with connection.cursor() as cursor:
                cursor.execute(f"CREATE DATABASE {db_settings['NAME']} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
                self.stdout.write(self.style.SUCCESS(f"Database '{db_settings['NAME']}' created successfully."))

            self.stdout.write(self.style.SUCCESS('Applying migrations...'))
            from django.core.management import call_command
            call_command('migrate')

            self.stdout.write(self.style.SUCCESS('Database creation and migration completed successfully.'))

        except mysql.connector.Error as e:
            self.stdout.write(self.style.ERROR(f'An error occurred: {e}'))

        finally:
            if connection:
                connection.close()
