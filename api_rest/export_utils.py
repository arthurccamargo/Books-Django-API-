import csv
from django.http import HttpResponse
from .models import Book, Rating

def export_books_csv():
    """
    Gera um arquivo CSV contendo dados dos livros
    """
    response = HttpResponse(content_type='text/csv')
    """
    Cabeçalho HTTP chamado Content-Disposition informa ao navegador que o conteúdo deve ser tratado como um arquivo para download
    filename="books.csv" nome padrão do arquivo para o navegador salvar
    """
    response['Content-Disposition'] = 'attachment; filename="books.csv"'

    writer = csv.writer(response)
    # Nome das colunas
    writer.writerow(['ID', 'Título', 'Autores', 'Descrição', 'Link', 'Nota Média', 'Total de Avaliações'])

    books = Book.objects.all() # Busca todos os registros da tabela 
    for book in books: # Escreve cada registro como uma linha no arquivo CSV
        writer.writerow([
            book.id,
            book.book_title,
            book.book_authors,
            book.book_description,
            book.book_selfLink,
            book.average_rating,
            book.rating_count
        ])
    return response # Retorna o arquivo CSV

def export_ratings_csv():
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="ratings.csv"'

    writer = csv.writer(response)
    writer.writerow(['ID', 'Livro', 'Pontuação', 'Comentário', 'Data de Criação'])

    ratings = Rating.objects.select_related('book').all()
    for rating in ratings:
        writer.writerow([
            rating.id,
            rating.book.book_title,
            rating.score,
            rating.comment,
            rating.created_at
        ])
    return response
