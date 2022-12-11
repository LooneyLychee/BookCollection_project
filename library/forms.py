from django import forms
from .models import Book, Author, PurchaseInfo, Series, Publisher
from django.forms import formset_factory


class BookModelForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('title', 'volume', 'publication_date', 'identifier',
                  'page_count', 'height', 'width', 'thickness', 'cover', 'categories',
                  'rating', 'notes')


class AuthorModelForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ('name',)


class PurchaseModelForm(forms.ModelForm):
    class Meta:
        model = PurchaseInfo
        fields = ('purchase_date', 'price',)


class SeriesModelForm(forms.ModelForm):
    class Meta:
        model = Series
        fields = ('name',)


class PublisherModelForm(forms.ModelForm):
    class Meta:
        model = Publisher
        fields = ('name',)


class AuthorDTOForm(forms.Form):
    name = forms.CharField(max_length=100)


AuthorDTOFormset = formset_factory(AuthorDTOForm, extra=1)
