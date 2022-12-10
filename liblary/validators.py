from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from six import string_types
from stdnum import isbn


def ISBNValidator(raw_isbn):
    isbn_to_check = raw_isbn.replace('-', '').replace(' ', '')

    if not isinstance(isbn_to_check, string_types):
        raise ValidationError(_(u'ISBN must be a string'))

    if len(isbn_to_check) != 10 and len(isbn_to_check) != 13:
        raise ValidationError(_(u'Wrong length'))

    if not isbn.is_valid(isbn_to_check):
        raise ValidationError(_(u'Invalid ISBN: Failed checksum'))

    if isbn_to_check != isbn_to_check.upper():
        raise ValidationError(_(u'Only upper case allowed'))

    return True
