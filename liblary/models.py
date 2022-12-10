from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from .validators import ISBNValidator


class Author(models.Model):
    author = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.author}'

    def get_books_number(self, collection):
        return self.book_set.all().filter(collection=collection).count()


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


class Category(models.Model):
    class Meta:
        verbose_name_plural = "categories"

    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)

    def __str__(self):
        return f'{self.category.title()}'

    def get_books_number(self, collection):
        return self.book_set.all().filter(collection=collection).count()


class Tag(models.Model):
    tag = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.tag}'

    def get_books_number(self, collection):
        return self.book_set.all().filter(collection=collection).count()


COLLECTION_CHOICES = (
    ('bookshelf', 'bookshelf'),
    ('wish_list', 'wish_list')
)


class Collection(models.Model):
    collection = models.CharField(max_length=20, choices=COLLECTION_CHOICES)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner')

    def __str__(self):
        return f'{self.collection} - {self.owner}'

    def get_books_number(self):
        return self.book_set.all().count()


class PurchaseInfo(models.Model):
    purchase_date = models.DateField(blank=True)
    price = models.DateField(blank=True)


class Book(models.Model):
    collections = models.ManyToManyField(Collection, related_name='collections')

    # basic info
    title = models.CharField(max_length=100)
    authors = models.ManyToManyField(Author, blank=True)
    series = models.CharField(max_length=100, null=True, blank=True)
    volume = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0.01)])

    # publication info
    publisher = models.CharField(max_length=50, blank=True)
    publication_date = models.DateField(blank=True)
    identifier = models.CharField(max_length=13, null=True, blank=True, validators=[ISBNValidator])

    # visual info
    page_count = models.PositiveSmallIntegerField(blank=True)
    height = models.FloatField(validators=[MinValueValidator(0.01)], blank=True)
    width = models.FloatField(blank=True, validators=[MinValueValidator(0.01)])
    thickness = models.FloatField(blank=True, validators=[MinValueValidator(0.01)])
    cover = models.ImageField(default='https://i.ibb.co/tKtFPgr/blank-profile-picture-g9a1ddb035-640.png', upload_to='avatars/')
    # find cover

    # content info
    categories = models.ManyToManyField(Category, blank=True)
    description = models.CharField(max_length=300, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)

    # purchase info
    purchase_info = models.OneToOneField(PurchaseInfo, on_delete=models.CASCADE, blank=True)

    # user personal info
    rating = models.PositiveSmallIntegerField(blank=True, validators=[MinValueValidator(0), MaxValueValidator(5)])
    notes = models.CharField(max_length=300, blank=True)

    update = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.authors}: {self.title}'


class ReadInfo(models.Model):
    volume = models.ForeignKey(Book, on_delete=models.CASCADE)
    start_date = models.DateField(blank=True)
    end_date = models.DateField(blank=True)


class LentInfo(models.Model):
    volume = models.ForeignKey(Book, on_delete=models.CASCADE)
    lent_date = models.DateField(blank=True)
    return_date = models.DateField(blank=True)
    borrower = models.CharField(max_length=100, null=True)
