from django.db import models

# Create your models here.
class Book(models.Model):
    id = models.AutoField(primary_key=True)  # Django gera IDs unicos
    book_title = models.CharField(max_length=100, default='', help_text="Título do livro")
    book_authors = models.CharField(max_length=150, default='', help_text="Nome do autor do livro")
    book_description = models.TextField(default='', help_text="Descrição do livro")
    book_selfLink = models.CharField(max_length=255, default='', help_text="Link do livro")

    def __str__(self) -> str:   
        return f'Title: {self.book_title} | Authors: {self.book_authors}'
