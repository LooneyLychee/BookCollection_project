from django.shortcuts import render, redirect
from django.http import HttpResponse


def home_view(request):
    return redirect('profiles:profile-list')

