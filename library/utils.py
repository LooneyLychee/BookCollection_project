from .filters import BookFilter
from .models import Book, Author

def search_in_book_info(books, query_param):
    if 'search' in query_param:
        phrase = query_param['search']
        books = books.filter(title__contains=phrase) | \
                books.filter(authors__name__contains=phrase) | \
                books.filter(series__name__contains=phrase) | \
                books.filter(description__contains=phrase) | \
                books.filter(notes__contains=phrase)

    return books


def order_by(books, query_param):
    if 'order_by' in query_param:
        criterion = query_param['order_by']
        books = books.order_by(criterion)

    return books


def filter(books, query_param):
    if 'authors' in query_param:
        authors_id = query_param.getlist('authors')
        books = books.filter(authors__id__in=list(authors_id))

    if 'publisher' in query_param:
        publishers_id = query_param.getlist('publisher')
        books = books.filter(publisher__id__in=list(publishers_id))

    if 'categories' in query_param:
        categories = query_param.get('categories')
        books = books.filter(categories__contains=categories)

    return books
