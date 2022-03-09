from csv import DictReader

from django.conf import settings
from django.core.management import BaseCommand
from reviews.models import Categories, Genre, GenreTitles, Titles

files_dict = {
    Categories: 'category.csv',
    GenreTitles: 'genre_title.csv',
    Genre: 'genre.csv',
    Titles: 'titles.csv'
}


class Command(BaseCommand):
    help = 'Loads data from csv'

    def handle(self, *args, **options):
        for model, files in files_dict.items():
            with open(
                f'{settings.BASE_DIR}/static/data/{files}', encoding='utf-8'
            ) as csv_file:
                df = DictReader(csv_file)
                model.objects.bulk_create(model(**row) for row in df)

        self.stdout.write(self.style.SUCCESS('Successfully'))
