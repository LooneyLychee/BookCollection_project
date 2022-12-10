from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Author)
admin.site.register(Collection)
admin.site.register(Category)
admin.site.register(Book)
admin.site.register(Tag)
admin.site.register(LentInfo)
admin.site.register(PurchaseInfo)
