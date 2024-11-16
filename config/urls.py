from django.contrib import admin
from django.urls import path
from django.urls.conf import include

urlpatterns = [
    path('', include('equity_hub.urls')),
    path('admin/', admin.site.urls, name='admin'),
    path('users/', include('users.urls')),
]
