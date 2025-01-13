import requests

def fetch_books_from_google(query):
    url = "https://www.googleapis.com/books/v1/volumes"
    params = {
        'q': query,  # Termo de busca
        'maxResults': 5,  # Limitar os resultados
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json().get('items', [])  # Retorna os livros encontrados
    else:
        raise Exception(f"Erro ao buscar dados: {response.status_code}")