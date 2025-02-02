from django import forms
from .models import *


class AddBookForm(forms.ModelForm):

    class Meta:
        model = Book
        fields = ['Title', 'Author', 'Year_Publishing', 'Count_Page', 'Cover', 'Publisher', 'Genre']
        labels = {
            'Title': 'Название',
            'Author': 'Автор',
            'Year_Publishing': 'Год публикации',
            'Count_Page': 'Количество страниц',
            'Cover': 'Обложка',
            'Publisher': 'Издатель',
            'Genre': 'Жанр',
        }


class AddReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ['Mark', 'Text_Review']
        labels = {
            'Mark': 'Your Mark',
            'Text_Review': 'Review',
        }

