from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('', views.get_books, name='get_all_book'),
    path('book/<int:id>', views.get_by_id, name='get_by_id')
]
