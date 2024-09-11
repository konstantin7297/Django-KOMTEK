import random
from sqlite3 import Date

from django.core.management import BaseCommand
from django.db import transaction, IntegrityError

from service_api.models import Directory, VersionDirectory, DirectoryElement


class Command(BaseCommand):
    """ Команда заполняет базу данных тестовыми записями. """
    @transaction.atomic
    def handle(self, *args, **options):
        try:
            self.stdout.write("Creates test data...")
            count = 9

            directories = [Directory.objects.get_or_create(
                code=f"Code{i}",
                name=f"Name{i}",
                description=f"Description{i}",
            ) for i in range(1, count + 1)]

            version_directories = [VersionDirectory.objects.get_or_create(
                directory=random.choice(directories)[0],
                version=f"{i}.0",
                created_date=Date(
                    year=random.randint(2010, 2024),
                    month=random.randint(1, 12),
                    day=random.randint(1, 28)
                ),
            ) for i in range(1, count + 1)]

            for i in range(1, count + 1):
                DirectoryElement.objects.get_or_create(
                    version_directory=random.choice(version_directories)[0],
                    code=f"Code{i}",
                    value=f"Value{i}",
                )

            self.stdout.write(self.style.SUCCESS(f"Data created."))
        except IntegrityError:
            self.stdout.write(self.style.ERROR(f"Data already exists."))
