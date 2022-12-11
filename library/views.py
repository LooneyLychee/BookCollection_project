from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import ListView
from .forms import AuthorDTOFormset

from profiles.models import Profile
from .forms import BookModelForm, AuthorModelForm, SeriesModelForm, PurchaseModelForm, PublisherModelForm
from .models import Book, Publisher, Author, PurchaseInfo, Series


def book_create_view(request):
    print(request.user)
    profile = Profile.objects.get(user=request.user)

    book_form = BookModelForm(request.POST or None, request.FILES or None, instance=obj, prefix='series')
    author_dto_form = AuthorDTOFormset(request.POST or None, prefix='series')
    author_form = AuthorModelForm(request.POST or None, request.FILES or None, instance=obj, prefix='author')
    publisher_form = PublisherModelForm(request.POST or None, request.FILES or None, instance=obj, prefix='series')
    purchase_form = PurchaseModelForm(request.POST or None, request.FILES or None, instance=obj, prefix='series')
    series_form = SeriesModelForm(request.POST or None, request.FILES or None, instance=obj, prefix='series')

    if request.method == 'POST':
        if 'add_author' in request.POST and author_form.is_valid():
            request.session.setdefault('authors', ())
            author = request.POST.get('author-name')

            if author not in request.session['authors']:
                request.session['authors'].append(author)

        if 'submit' in request.POST and author_form.is_valid() and book_form.is_valid():
            book_form.save()
            book = book_form.instance

            request.session.setdefault('authors', ())
            authors = request.session['authors']
            existing_authors = profile.get_all_authors()

            for author in authors:
                if author not in existing_authors:
                    author1 = Author.objects.create(name=author.name)
                    book.authors.add(author1)
    return render(request, 'profiles/my_profile.html', context)
