from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('books/', views.book_list, name='book_list'),
    path('data/<int:id>', views.book_manager, name='book_manager')
]
