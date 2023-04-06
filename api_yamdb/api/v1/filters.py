from django_filters import Filter, FilterSet

from reviews.models import Title


class GenreFilter(Filter):
    """Фильтр для поиска по жанрам произведений."""

    def filter(self, qs, value):
        if not value:
            return qs
        return qs.filter(genre__slug__icontains=value)


class CategoryFilter(Filter):
    """Фильтр для поиска по категориям произведений."""

    def filter(self, qs, value):
        if not value:
            return qs
        return qs.filter(category__slug__icontains=value)


class TitleNameFilter(Filter):
    """Фильтр для поиска по названиям произведений."""

    def filter(self, qs, value):
        if not value:
            return qs
        return qs.filter(name__icontains=value)


class TitleYearFilter(Filter):
    """Фильтр для поиска по году выпуска произведения."""

    def filter(self, qs, value):
        if not value:
            return qs
        return qs.filter(year__exact=value)


class TitleFilter(FilterSet):
    """Основной класс кастомного фильтра.

    Фильтрация по жанру, категории, названию или году выпуска.
    """

    genre = GenreFilter(field_name="genre")
    category = CategoryFilter(field_name="category")
    name = TitleNameFilter(field_name="name")
    year = TitleYearFilter(field_name="year")

    class Meta:
        model = Title
        fields = {
            "genre": ["exact"],
            "category": ["exact"],
            "name": ["icontains"],
            "year": ["exact"],
        }
