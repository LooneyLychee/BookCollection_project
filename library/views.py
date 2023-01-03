import requests
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import ListView
from django.core.paginator import Paginator
from django_filters import  filters
from .forms import AuthorDTOFormset
from .utils import search_in_book_info, order_by, filter
from profiles.models import Profile
from profiles.views import upload_file
from .forms import CollectionModelForm, BookModelForm, AuthorModelForm, SeriesModelForm, PurchaseModelForm, PublisherModelForm
from .models import Book, Publisher, Author, PurchaseInfo, Series, Collection, CATEGORY_CHOICES
from .filters import BookFilter
from django.forms.models import model_to_dict
import base64


def add_author_to_list(request, author_name):
    if 'authors' not in request.session:
        request.session['authors'] = []

    authors = request.session['authors']
    if author_name not in authors:
        authors.append(author_name)
        request.session['authors'] = authors


def remove_author_from_list(request, author_name):
    authors = request.session['authors']
    if author_name in authors:
        authors.remove(author_name)
        request.session['authors'] = authors


def get_authors(request):
    if 'authors' not in request.session:
        request.session['authors'] = []

    return request.session['authors']


def are_forms_valid(forms):
    for form in forms:
        if not form.is_valid():
            return False

    return True


def book_create_or_update_view(request, book_id=None):
    profile = Profile.objects.get(user=request.user)

    if book_id:
        book = Book.objects.get(id=book_id)
        publisher = book.publisher
        series = book.series
        purchase = book.purchase_info
        collections = {}
        collections = book.collection.all().values('name')[0]['name']
        if 'authors' not in request.session:
            for author in book.authors.all():
                add_author_to_list(request, author.name)
    else:
        book = None
        publisher = None
        series = None
        purchase = None
        collections = None

    book_form = BookModelForm(request.POST or None, request.FILES or None, instance=book, prefix='book')
    authors_form = AuthorModelForm(request.POST or None, request.FILES or None, prefix='author')
    publisher_form = PublisherModelForm(request.POST or None, request.FILES or None, instance=publisher, prefix='publisher')
    purchase_form = PurchaseModelForm(request.POST or None, request.FILES or None, instance=purchase, prefix='purchase')
    series_form = SeriesModelForm(request.POST or None, request.FILES or None, instance=series, prefix='series')
    forms = [purchase_form, publisher_form, series_form]
    book_form.fields['collections'].initial = collections

    if request.method == 'POST':
        if 'remove-author' in request.POST and authors_form.is_valid():
            author = request.POST.get('remove-author')
            remove_author_from_list(request, author)

        elif 'add-author' in request.POST and authors_form.is_valid():
            author = request.POST.get('author-name')
            add_author_to_list(request, author)

        elif ('submit' in request.POST or 'submit-default' in request.POST) and book_form.is_valid() and are_forms_valid(forms):
            book_form.save()
            book = book_form.instance

            if 'book-image' in request.FILES:
                image = base64.b64encode(request.FILES['book-image'].read())
                book.cover = upload_file(image)
                print(book.cover)

            elif 'submit-default' in request.POST:
                book.cover = 'https://i.ibb.co/s2THm06/no-image-icon-23480.jpg'
                print(book.cover)

            book.collection.clear()
            for collection in request.POST.getlist('book-collections'):
                collection = profile.get_collection(collection)
                collection.books.add(book)
                collection.owner = profile
                collection.save()

            book.authors.clear()
            authors = get_authors(request)
            existing_authors = profile.get_all_authors()

            for author in authors:
                if author not in existing_authors:
                    author1 = Author.objects.create(name=author)
                else:
                    author1 = profile.get_author(author)

                book.authors.add(author1)

            if request.POST.get('publisher-name') != '':
                publisher = profile.get_publisher(request.POST.get('publisher-name'))

                if publisher is None:
                    publisher = publisher_form.save()

                book.publisher = publisher
            else:
                book.publisher = None

            if request.POST.get('series-name') != '':
                series = profile.get_series(request.POST.get('series-name'))
                if series is None:
                    series = series_form.save()

                book.series = series
            else:
                book.series = None

            if request.POST.get('purchase-purchase_date') != '' and request.POST.get('purchase-purchase_price') != '':
                purchase = purchase_form.save()
                book.purchase_info = purchase
            else:
                purchase_form = None

            book.save()

            request.session.delete('authors')
            return redirect("library:book", book_id=book.id, collection_id=collection.id)

    authors = get_authors(request)

    context = {
        'authors_form': authors_form,
        'profile': profile,
        'authors': authors,
        'book_form': book_form,
        'series_form': series_form,
        'publisher_form': publisher_form,
        'purchase_form': purchase_form,
    }

    return render(request, 'library/book_create.html', context)


def collection_view(request, collection_id):

    books = Collection.objects.get(id=collection_id).books.all()
    collection = Collection.objects.get(id=collection_id)

    filterset = BookFilter(request.GET, books)
    books = filter(books, request.GET)

    books = search_in_book_info(books, request.GET)
    print(books)
    books = order_by(books, request.GET)

    paginator = Paginator(books.distinct(), 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'filterset': filterset,
        'collection': collection,
        'category_choices': list(next(zip(*CATEGORY_CHOICES)))
    }

    return render(request, 'library/collection.html', context)


def book_view(request, collection_id, book_id):
    book = Book.objects.get(pk=book_id)
    collection = Collection.objects.get(id=collection_id)
    owner = Profile.objects.get(id=collection.owner_id).user
    context = {
        'book': book,
        'owner': owner,
        'collection': collection,
    }

    return render(request, 'library/book.html', context)


def book_delete(request, book_id, collection_id):
    book = Book.objects.get(id=book_id)
    collection = Collection.objects.get(id=collection_id)
    collection.books.remove(book)

    if not book.collection.all():
        book.delete()

    return redirect("library:book-list", collection_id=collection_id)


