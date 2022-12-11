from django.db import models
from django.contrib.auth.models import User
from .utils import get_random_code
from django.template.defaultfilters import slugify
import datetime


class Profile(models.Model):
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=150, blank=True)
    avatar = models.ImageField(default='https://i.ibb.co/tKtFPgr/blank-profile-picture-g9a1ddb035-640.png', upload_to='avatars/')
    following = models.ManyToManyField(User, blank=True, related_name='following')
    followers = models.ManyToManyField(User, blank=True, related_name='followers')
    slug = models.SlugField(unique=True, blank=True)
    update = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}-{self.created}"

    def get_my_books_number(self):
        collection = list(self.collection.filter(name="bookshelf"))
        try:
            return collection[0].get_books_number()
        except:
            return 'no date'

    def get_wish_list_books_number(self):
        collection = list(self.collection.filter(name="wish_list"))
        try:
            return collection[0].get_books_number()
        except:
            return 'no date'

    def get_favorites_books_number(self):
        collection = list(self.collection.filter(name="favorites"))
        try:
            return collection[0].get_books_number()
        except:
            return 'no date'

    def get_all_authors(self):
        return self.collection.values('books__authors__name')

    def get_authors_number_bookshelf(self):
        collection = list(self.collection.filter(name="bookshelf"))
        try:
            return collection[0].get_authors_number()
        except:
            return 'no date'

    def get_series_number_bookshelf(self):
        collection = list(self.collection.filter(name="bookshelf"))
        try:
            return collection[0].get_series_number()
        except:
            return 'no date'

    def get_publisher_number_bookshelf(self):
        collection = list(self.collection.filter(name="bookshelf"))
        try:
            return collection[0].get_publisher_number()
        except:
            return 'no date'

    def get_books_read_number_bookshelf(self):
        collection = list(self.collection.filter(name="bookshelf"))
        try:
            return collection[0].get_books_read_number()
        except:
            return 'no date'

    def get_followers(self):
        return self.followers.all()

    def get_following(self):
        return self.following.all()

    def get_followers_number(self):
        return self.followers.all().count()

    def get_following_number(self):
        return self.following.all().count()

    def save(self, *args, **kwargs):
        ex = False
        if self.first_name and self.last_name:
            to_slug = slugify(str(self.first_name) + " " + str(self.last_name))
            ex = Profile.objects.filter(slug=to_slug).exists()
        else:
            to_slug = str(self.user.username)

        self.slug = to_slug
        self.update = datetime.datetime.now()
        super().save(*args, **kwargs)


class Follow(models.Model):
    follower = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='follower')
    followee = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='followee')
    update = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.follower}-{self.followee}"
