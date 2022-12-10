
from django.contrib import admin
from django.urls import path, include
from .views import my_profile_view

app_name = 'profiles'

urlpatterns = [
    path('myprofile/', my_profile_view, name='my-profile'),
]
