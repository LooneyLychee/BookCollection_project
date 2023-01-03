
from django.contrib import admin
from django.template.defaulttags import url
from django.urls import path, include
from .views import profile_view, profiles_list_view

app_name = 'profiles'

urlpatterns = [
    path('profile/<profile_id>/', profile_view, name='profile'),
    path('', profiles_list_view, name='profile-list'),
]
