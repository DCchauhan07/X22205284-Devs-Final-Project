"""Doctype"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.contrib.auth import views # pylint: disable=unused-import
from django.conf.urls.static import static

urlpatterns = [
    path('', include('core.urls')),
    path('cart/', include('cart.urls')),
    path('order/', include('order.urls')),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
