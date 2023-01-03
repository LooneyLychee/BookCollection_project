import django_filters
from .models import Book, Collection, CATEGORY_CHOICES
from rest_framework import filters
from django import forms


class BookFilter(django_filters.FilterSet):
    # categories = django_filters.MultipleChoiceFilter(choices=CATEGORY_CHOICES, field_name='categories')
    class Meta:
        model = Book
        fields = ['categories', 'series', 'publisher', 'authors']


