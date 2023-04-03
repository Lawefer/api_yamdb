import os
import csv

from reviews.models import (Category,
                            Comment,
                            Genre,
                            Review,
                            Title,
                            User,)

from adaptor.model import CsvDbModel

class CategoryCSV(CsvDbModel):
    class Meta:
       dbModel = Category
       delimiter = ";"


CSV_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'static', 'data'
)


CSV_DB_TABLE = {
    #User: os.path.join(CSV_DIR, 'users.csv'),
    CategoryCSV: os.path.join(CSV_DIR, 'category.csv'),
    #Genre: os.path.join(CSV_DIR, 'genre.csv'),
    #Title: os.path.join(CSV_DIR, 'titles.csv'),
    #Review: os.path.join(CSV_DIR, 'review.csv'),
    #Comment: os.path.join(CSV_DIR, 'comments.csv'),
}


def read_csv_file(filename):
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        return [row for row in reader]


def run():
    print('1))')
    my_csv_list = CategoryCSV.import_data(data=open(os.path.join(os.path.dirname(CSV_DIR), 'category.csv')))
    first_line = my_csv_list[0]
    print(first_line.id)
    #for model_class, filename in CSV_DB_TABLE.items():
    #    model_class.import_data(data = open(filename))
