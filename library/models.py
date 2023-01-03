from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from .validators import ISBNValidator
from multiselectfield import MultiSelectField
import datetime
from profiles.models import Profile
from django_select2.forms import Select2MultipleWidget


class Author(models.Model):
    name = models.CharField(max_length=100, blank=True, default="")

    def __str__(self):
        return f'{self.name}'


CATEGORY_CHOICES = (
                       ('nonclassifiable', 'nonclassifiable'),
                       ('antiques & collectibles', 'antiques & collectibles'),
                       ('architecture', 'architecture'),
                       ('art', 'art'),
                       ('bibles', 'bibles'),
                       ('biography & autobiography', 'biography & autobiography'),
                       ('body, mind & spirit', 'body, mind & spirit'),
                       ('business & economics', 'business & economics'),
                       ('comics and graphics', 'comics and graphics'),
                       ('novels', 'novels'),
                       ('computers', 'computers'),
                       ('cooking', 'cooking'),
                       ('craft & hobbies', 'craft & hobbies'),
                       ('design', 'design'),
                       ('drama', 'drama'),
                       ('education', 'education'),
                       ('family_relationships', 'family_relationships'),
                       ('fiction', 'fiction'),
                       ('foreign', 'foreign'),
                       ('language', 'language'),
                       ('study', 'study'),
                       ('games_activities', 'games_activities'),
                       ('gardening', 'gardening'),
                       ('health & fitness', 'health & fitness'),
                       ('history', 'history'),
                       ('house & home', 'house & home'),
                       ('humor', 'humor'),
                       ('juvenile fiction', 'juvenile fiction'),
                       ('juvenile nonfiction', 'juvenile nonfiction'),
                       ('language arts & disciplines', 'language arts & disciplines'),
                       ('law', 'law'),
                       ('literary collections', 'literary collections'),
                       ('literary_criticism', 'literary_criticism'),
                       ('mathematics', 'mathematics'),
                       ('medical', 'medical'),
                       ('music', 'music'),
                       ('nature', 'nature'),
                       ('performing', 'performing'),
                       ('arts', 'arts'),
                       ('pets', 'pets'),
                       ('philosophy', 'philosophy'),
                       ('photography', 'photography'),
                       ('poetry', 'poetry'),
                       ('political_science', 'political_science'),
                       ('psychology', 'psychology'),
                       ('reference', 'reference'),
                       ('religion', 'religion'),
                       ('science', 'science'),
                       ('self_help', 'self_help'),
                       ('social_science', 'social_science'),
                       ('sports &recreation', 'sports &recreation'),
                       ('study_aids', 'study_aids'),
                       ('technology_end_engineering', 'technology_end_engineering'),
                       ('transportation', 'transportation'),
                       ('travel', 'travel'),
                       ('true crime', 'true crime'),
                       ('young adult fiction', 'young adult fiction'),
                       ('young adult nonfiction', 'young adult nonfiction')
)

RATING_CHOICES = (
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
    ('6', '6'),
    ('7', '7'),
    ('8', '8'),
    ('9', '9'),
    ('10', '10'),
)

class Tag(models.Model):
    tag = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.tag}'


COLLECTION_CHOICES = (
    ('bookshelf', 'bookshelf'),
    ('wish_list', 'wish_list'),
    ('favorites', 'favorites')
)


class PurchaseInfo(models.Model):
    class Meta:
        verbose_name_plural = "Purchase_Info"

    purchase_date = models.DateField(blank=True, null=True)
    price = models.FloatField(validators=[MinValueValidator(0)], null=True, blank=True)

    def __str__(self):
        return f'{self.purchase_date}'


class Series(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f'{self.name}'


class Publisher(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f'{self.name}'


class Book(models.Model):
    # basic info
    title = models.CharField(max_length=100)
    authors = models.ManyToManyField(Author, blank=True, related_name='book')
    series = models.ForeignKey(Series, on_delete=models.CASCADE, null=True, blank=True, related_name='book')
    volume = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0.01)])

    # publication info
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE, null=True, blank=True, related_name='book')
    publication_date = models.DateField(blank=True, null=True)
    identifier = models.CharField(max_length=13, blank=True, validators=[ISBNValidator], null=True)

    # visual info
    page_count = models.PositiveSmallIntegerField(blank=True, default="", null=True)
    height = models.FloatField(validators=[MinValueValidator(0.01)], blank=True, null=True)
    width = models.FloatField(blank=True, null=True, validators=[MinValueValidator(0.01)])
    thickness = models.FloatField(blank=True, null=True, validators=[MinValueValidator(0.01)])
    cover = models.CharField(max_length=150, default='https://i.ibb.co/s2THm06/no-image-icon-23480.jpg')
    # find cover

    # content info
    categories = MultiSelectField(choices=CATEGORY_CHOICES, blank=True, max_choices=30, max_length=600, null=True)
    description = models.CharField(max_length=1000, blank=True, null=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name='book')

    # purchase info
    purchase_info = models.OneToOneField(PurchaseInfo, on_delete=models.CASCADE, null=True, blank=True, related_name='book')

    # user personal info
    rating = models.CharField(max_length=9, choices=RATING_CHOICES, blank=True, null=True)
    notes = models.CharField(max_length=1000, blank=True, null=True)

    update = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title}'


class Collection(models.Model):
    name = models.CharField(max_length=20, choices=COLLECTION_CHOICES)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='collection')
    books = models.ManyToManyField(Book, blank=True, null=True, related_name='collection')

    def __str__(self):
        return f"{str(self.owner)}: {self.name}"


    def get_books_number(self):
        return self.books.all().count()

    def get_authors_number(self):
        books = self.books.exclude(authors__isnull=True)
        authors = []
        for book in books:
            authors += list(book.authors.all())

        return len(set(authors))

    def get_series_number(self):
        return len(set(self.books.exclude(series__isnull=True).values_list('series')))

    def get_publisher_number(self):
        return len(set(self.books.exclude(publisher__isnull=True).values_list('publisher')))

    def get_books_read_number(self):
        read_info = self.books.exclude(read_info__isnull=True).values_list('read_info')
        return len(set(read_info.values_list('volume')))

    def get_authors(self):
        authors = None

        for book in self.books.all():
            new_authors = book.authors.all()
            if new_authors and authors:
                authors = authors.union(new_authors)
            elif new_authors:
                authors = new_authors

        return authors

    def get_series(self):
        series = []

        for book in self.books.all():
            new_series = book.series
            if new_series:
                series.append(new_series)

        return series

    def get_publisher(self):
        publisher = []

        for book in self.books.all():
            new_publisher = book.publisher
            if new_publisher:
                publisher.append(new_publisher)

        return publisher


class ReadInfo(models.Model):
    class Meta:
        verbose_name_plural = "Read_Info"

    volume = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="read_info")
    start_date = models.DateField(blank=True)
    end_date = models.DateField(blank=True)

    def __str__(self):
        return f'{self.volume}: {self.start_date} - {self.end_date}'


class LentInfo(models.Model):
    class Meta:
        verbose_name_plural = "Lent_Info"

    volume = models.ForeignKey(Book, on_delete=models.CASCADE)
    lent_date = models.DateField(blank=True)
    return_date = models.DateField(blank=True)
    borrower = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f'{self.borrower} - {self.volume}'
