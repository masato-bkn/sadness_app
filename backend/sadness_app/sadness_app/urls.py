# coding: utf-8

from django.contrib import admin
from django.urls import path, include

# from emotion.urls import router as emotion_router

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('api/', include('emotion.urls')),
]