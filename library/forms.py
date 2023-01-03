from django import forms
from django_select2.forms import Select2MultipleWidget

from .models import Book, Author, PurchaseInfo, Series, Publisher, Collection, COLLECTION_CHOICES
from django.forms import formset_factory


class CollectionModelForm(forms.ModelForm):
    class Meta:
        model = Collection
        fields = ('name', )


class DateInput(forms.DateInput):
    input_type = 'date'


class BookModelForm(forms.ModelForm):
    image = forms.FileField(required=False)
    collections = forms.MultipleChoiceField(required=True, widget=forms.CheckboxSelectMultiple, choices=COLLECTION_CHOICES)

    class Meta:
        model = Book
        fields = ('title', 'volume', 'publication_date', 'description', 'identifier',
                  'page_count', 'height', 'width', 'thickness', 'cover', 'categories',
                  'rating', 'notes')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'notes': forms.Textarea(attrs={'rows': 4}),
            'categories': forms.CheckboxSelectMultiple,
            'rating': forms.RadioSelect,
            'publication_date': DateInput(),
        }

    def __init__(self, *args, **kwargs):
        super(BookModelForm, self).__init__(*args, **kwargs)

        self.fields['cover'].required = False


class AuthorModelForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ('name',)


class PurchaseModelForm(forms.ModelForm):
    class Meta:
        model = PurchaseInfo
        fields = ('purchase_date', 'price',)
        widgets = {
            'purchase_date': DateInput(),
        }


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
