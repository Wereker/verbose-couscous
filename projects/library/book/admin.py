from django.contrib import admin
from .models import *


class BookAdmin(admin.ModelAdmin):

    # Без явного перечисления полей модели User будет выводиться
    # список коллекций
    list_display = [field.name for field in Book._meta.fields]

    # Поля в таблице редактируемые
    list_editable = ('Price', 'Genre', 'Title')

    # Список полей, по которым будет поиск в таблице
    search_fields = ['Title', 'Genre', 'Author']

    # Список полей, по которым будут фильтроваться записи в админке (панель)
    list_filter = ['Genre', 'Author']

    class Meta:
        model = Book


class GenreAdmin(admin.ModelAdmin):

    list_display = [field.name for field in Genre._meta.fields]

    list_editable = ('Name', 'Description', 'Image')

    search_fields = ['Name']

    class Meta:
        model = Genre


class AuthorAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Author._meta.fields]

    list_editable = ('First_Name', 'Last_Name', 'Pseudonym', 'Biography')

    search_fields = ['First_Name', 'Last_Name']

    class Meta:
        model = Author


class ReviewAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Review._meta.fields]

    list_editable = ('Book', 'User', 'Mark', 'Text_Review')

    search_fields = ['Book', 'Mark']

    class Meta:
        model = Review


# Register your models here.
admin.site.register(Book, BookAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Review, ReviewAdmin)


