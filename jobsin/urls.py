from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('jobsearch.urls')),
    path(r'auth/', include('djoser.urls')),
    path(r'auth/', include('djoser.urls.jwt')),
]