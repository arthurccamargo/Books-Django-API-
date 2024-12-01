from django.db import models

# Create your models here.
class Book(models.Model):
    book_id = models.IntegerField(primary_key=True)
    book_title = models.CharField(max_length=100, default='')
    book_authors = models.CharField(max_length=150, default='')
    book_description = models.TextField(default='')
    book_selfLink = models.CharField(max_length=100, default='')


    def __str__(self) -> str:
        return f'Title: {self.book_title} | Authors: {self.book_authors}'
