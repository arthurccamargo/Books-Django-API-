from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Book(models.Model):
    id = models.AutoField(primary_key=True)  # Django gera IDs unicos
    book_title = models.CharField(max_length=100, default='', help_text="Título do livro")
    book_authors = models.CharField(max_length=150, default='', help_text="Nome do autor do livro")
    book_description = models.TextField(default='', help_text="Descrição do livro")
    book_selfLink = models.CharField(max_length=255, default='', help_text="Link do livro")
    average_rating = models.FloatField(default=0.0)  # Nota média dos livros
    rating_count = models.PositiveIntegerField(default=0)  # Total de avaliações

    """
    classe interna usada para definir metadados ou configurações do modelo
    controlam o comportamento e as regras aplicadas ao modelo no banco de dados ou na aplicação
    """
    class Meta:
        constraints = [
            # Garante unicidade de título + autor
            models.UniqueConstraint(fields=['book_title', 'book_authors'], name='unique_book_title_author')
        ] 

    def __str__(self) -> str:   
        return f'Title: {self.book_title} | Authors: {self.book_authors}'
    
class Rating(models.Model):
    book = models.ForeignKey('Book', on_delete=models.CASCADE, related_name='ratings')
    # Score deve ser um numero inteiro positivo entre  0 e 5
    score = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:   
        return f'Book: {self.book} | Score: {self.score}'
