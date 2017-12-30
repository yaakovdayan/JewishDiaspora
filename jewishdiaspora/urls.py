from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.views.i18n import JavaScriptCatalog

from artifacts import views
from users import views as user_views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('register/', user_views.UserFormView.as_view(), name='register'),
    path('contact', user_views.ContactView.as_view(), name='contact'),
    path('about', views.AboutView.as_view(), name='about'),
    path('admin/', admin.site.urls),
    path('artifact/', include('artifacts.urls')),
    path('accounts/', include('authtools.urls')),
    path('jsi18n/', JavaScriptCatalog.as_view(packages=['artifacts']), name='javascript-catalog'),
    path('i18n/', include('django.conf.urls.i18n')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
