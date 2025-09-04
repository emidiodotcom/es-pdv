from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('admin/',  admin.site.urls, ),
    path('login/',  views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('',        views.order, name='order'),
]

admin.site.site_header = 'PDV - Administração'

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
