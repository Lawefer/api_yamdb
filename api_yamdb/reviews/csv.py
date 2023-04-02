import os
import csv

from reviews.models import (Category,
                            Comment,
                            Genre,
                            Review,
                            Title,
                            User,
                            Title_Genre)
                   
CSV_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'data')

CSV_DB_TABLE = {
    User: os.path.join(CSV_DIR, 'users.csv'),
    Category: os.path.join(CSV_DIR, 'category.csv'),
    Genre: os.path.join(CSV_DIR, 'genre.csv'),
    Title: os.path.join(CSV_DIR, 'titles.csv'),
    Review: os.path.join(CSV_DIR, 'review.csv'),
    Comment: os.path.join(CSV_DIR, 'comments.csv'),
    Title_Genre: os.path.join(CSV_DIR, 'genre_title.csv'),
}


def read_csv_file(filename):
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        return [row for row in reader]


def import_data():
    for model_class, filename in CSV_DB_TABLE.items():
        rows = read_csv_file(filename)
        instances = [model_class(**row) for row in rows]
        model_class.objects.bulk_create(instances)


if __name__ == '__main__':
    import_data()