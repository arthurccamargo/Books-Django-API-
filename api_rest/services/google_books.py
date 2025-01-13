import requests
from api_rest.models import Book
from api_rest.serializers import BookSerializer
import logging

logger = logging.getLogger(__name__)

# Busca livros na API do Google Books com base no termo de busca.
def fetch_books_from_google(query):
    logger.info(f"Iniciando busca por livros com o termo: {query}")
    
    url = "https://www.googleapis.com/books/v1/volumes"
    params = {
        'q': query,  # Termo de busca
        'maxResults': 5,  # Limitar os resultados
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json().get('items', [])
    else:
        raise Exception(f"Erro ao buscar dados: {response.status_code}")

#  Busca livros na API do Google Books e salva no banco de dados.
def save_books_to_db(query):
    # Buscar livros na API do Google Books
    books_data = fetch_books_from_google(query)

    # Lista para armazenar os objetos criados
    created_books = []

    for book in books_data:
        # Extrair os dados relevantes de cada livro retornado pela API
        volume_info = book.get('volumeInfo', {})
        new_book_data = {
            'book_title': volume_info.get('title', 'Sem título'),
            'book_authors': ', '.join(volume_info.get('authors', [])),
            'book_description': volume_info.get('description', 'Sem descrição'),
            'book_selfLink': book.get('selfLink', None),
        }

        # Verificar se o livro possui selfLink e se já existe no banco com base no selfLink
        if new_book_data['selfLink'] and not Book.objects.filter(selfLink=new_book_data['selfLink']).exists():
            serializer = BookSerializer(data=new_book_data)
            if serializer.is_valid():
                created_book = serializer.save()
                created_books.append(created_book)

    return created_books