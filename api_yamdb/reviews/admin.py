from django.contrib import admin

from .models import Comment, Review, Rating, Title, Genre, Category


class ReviewAdmin(admin.ModelAdmin):
    list_display = ("pk", "text", "pub_date", "author",)
    search_fields = ("text",)
    list_filter = ("pub_date",)
    list_editable = ("text",)
    empty_value_display = "-пусто-"


class CommentAdmin(admin.ModelAdmin):
    list_display = ("pk", "review", "text", "author", "pub_date")
    search_fields = ("text",)
    list_filter = ("pub_date",)
    list_editable = ("text",)
    empty_value_display = "-пусто-"


class RatingAdmin(admin.ModelAdmin):
    list_display = ("pk", "title", "user", "grade")
    search_fields = ("user",)
    empty_value_display = "-пусто-"

class TitleAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", 'year', 'description', 'category')
    search_fields = ('name',)
    list_editable = ('name',)

class GenreAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", 'slug')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("pk", "name",'slug')

admin.site.register(Title, TitleAdmin)
admin.site.register(Rating, RatingAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Category, CategoryAdmin)