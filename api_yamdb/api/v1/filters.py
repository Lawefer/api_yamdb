from django_filters import Filter, FilterSet

from reviews.models import Title


class GenreFilter(Filter):
    def filter(self, qs, value):
        if not value:
            return qs
        return qs.filter(genre__slug__icontains=value)


class CategoryFilter(Filter):
    def filter(self, qs, value):
        if not value:
            return qs
        return qs.filter(category__slug__icontains=value)


class TitleNameFilter(Filter):
    def filter(self, qs, value):
        if not value:
            return qs
        return qs.filter(name__icontains=value)


class TitleYearFilter(Filter):
    def filter(self, qs, value):
        if not value:
            return qs
        return qs.filter(year__exact=value)


class TitleFilter(FilterSet):
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
