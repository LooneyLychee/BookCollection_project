from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import home_view
from profiles import urls as profiles_urls
from library import urls as library_urls
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('profiles/', include(profiles_urls, namespace='profiles')),
    path('library/', include(library_urls, namespace='library')),
    path('', home_view),
    path('accounts/', include('allauth.urls')),
    path('logout', LogoutView.as_view()),

]

#urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
