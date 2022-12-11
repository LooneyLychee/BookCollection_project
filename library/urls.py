
from django.contrib import admin
from django.urls import path, include
from .views import book_create_view

app_name = 'profiles'

urlpatterns = [
    path('book-create/', book_create_view, name='book-create'),
]
