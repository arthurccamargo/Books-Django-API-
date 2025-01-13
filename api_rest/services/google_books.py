import requests
from api_rest.models import Book
from api_rest.serializers import BookSerializer

# Busca livros na API do Google Books com base no termo de busca.
# Livros só serão salvos se todos os atributos exigidos pelo modelo estiverem presentes e válidos.
def fetch_books_from_google(query):
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
        # Verificar se 'selfLink' existe no objeto
        if 'selfLink' not in book:
            continue

        volume_info = book.get('volumeInfo', {})

        # Extrair os dados necessários
        new_book_data = {
            'book_title': volume_info.get('title'),
            'book_authors': ', '.join(volume_info.get('authors', [])),
            'book_description': volume_info.get('description'),
            'book_selfLink': book.get('selfLink'),
        }

        # Verificar se todos os campos necessários estão presentes
        if all(new_book_data.values()) and not Book.objects.filter(book_selfLink=new_book_data['book_selfLink']).exists():
            serializer = BookSerializer(data=new_book_data)
            if serializer.is_valid():
                created_book = serializer.save()
                created_books.append(created_book)

    return created_books