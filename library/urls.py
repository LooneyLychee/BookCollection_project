
from django.contrib import admin
from django.urls import path, include
from .views import book_create_or_update_view, collection_view, book_view, book_delete

app_name = 'library'

urlpatterns = [
    path('book-create/', book_create_or_update_view, name='book-create'),
    path('book-update/<str:book_id>', book_create_or_update_view, name='book-update'),
    path("select2/", include("django_select2.urls")),
    path("collection/<str:collection_id>/", collection_view, name='book-list'),
    path("book/<collection_id>/<str:book_id>/", book_view, name='book'),
    path("book-delete/<collection_id>/<str:book_id>/", book_delete, name='book-delete')
]
