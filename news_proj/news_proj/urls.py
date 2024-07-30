from django.contrib import admin
from django.urls import path, include
from news import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('news.urls')),
]

handler404 = views.custom_404