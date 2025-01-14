from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from .models import Book, Rating
from .serializers import BookSerializer, RatingSerializer

class BookViewSetTests(APITestCase):
    def setUp(self):
        # Criar um usuário para testes de endpoints autenticados
        self.user = User.objects.create_user(
            username='arthur',
            password='senhasenha'
        )
        self.client = APIClient()
        
        # Criar alguns livros para teste
        self.book1 = Book.objects.create(
            book_title='O Senhor dos Anéis',
            book_authors='J.R.R. Tolkien',
            book_description='Uma aventura épica',
            book_selfLink='http://exemplo.com/livro1'
        )
        
        self.book2 = Book.objects.create(
            book_title='O Hobbit',
            book_authors='J.R.R. Tolkien',
            book_description='A jornada inicial',
            book_selfLink='http://exemplo.com/livro2'
        )

    def test_list_books(self):
        """
        Teste para listar livros (não requer autenticação)
        """
        url = reverse('book-list')
        response = self.client.get(url)
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], serializer.data)

    def test_retrieve_book(self):
        """
        Teste para recuperar um livro específico (não requer autenticação)
        """
        url = reverse('book-detail', kwargs={'pk': self.book1.pk})
        response = self.client.get(url)
        book = Book.objects.get(pk=self.book1.pk)
        serializer = BookSerializer(book)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_book_authenticated(self):
        """
        Teste para criar um livro (requer autenticação)
        """
        self.client.force_authenticate(user=self.user)
        url = reverse('book-list')
        data = {
            'book_title': 'Duna',
            'book_authors': 'Frank Herbert',
            'book_description': 'Ficção científica épica',
            'book_selfLink': 'http://exemplo.com/livro3'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)

    def test_create_book_unauthenticated(self):
        """
        Teste para criar um livro sem autenticação (deve falhar)
        """
        url = reverse('book-list')
        data = {
            'book_title': 'Duna',
            'book_authors': 'Frank Herbert',
            'book_description': 'Ficção científica épica',
            'book_selfLink': 'http://exemplo.com/livro3'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_book_authenticated(self):
        """
        Teste para atualizar um livro (requer autenticação)
        """
        self.client.force_authenticate(user=self.user)
        url = reverse('book-detail', kwargs={'pk': self.book1.pk})
        data = {
            'book_title': 'O Senhor dos Anéis - Edição Atualizada',
            'book_authors': 'J.R.R. Tolkien',
            'book_description': 'Uma aventura épica - versão revisada',
            'book_selfLink': 'http://exemplo.com/livro1'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.book_title, 'O Senhor dos Anéis - Edição Atualizada')

    def test_delete_book_authenticated(self):
        """
        Teste para deletar um livro (requer autenticação)
        """
        self.client.force_authenticate(user=self.user)
        url = reverse('book-detail', kwargs={'pk': self.book1.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)

class RatingViewSetTests(APITestCase):
    def setUp(self):
        # Criar usuário para testes
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client = APIClient()
        
        # Criar um livro para teste
        self.book = Book.objects.create(
            book_title='O Senhor dos Anéis',
            book_authors='J.R.R. Tolkien',
            book_description='Uma aventura épica',
            book_selfLink='http://exemplo.com/livro1'
        )
        
        # Criar algumas avaliações para teste
        self.rating1 = Rating.objects.create(
            book=self.book,
            score=5,
            comment='Excelente livro!'
        )
        
        self.rating2 = Rating.objects.create(
            book=self.book,
            score=4,
            comment='Muito bom!'
        )

    def test_list_ratings(self):
        """
        Teste para listar avaliações (não requer autenticação)
        """
        url = reverse('rating-list')
        response = self.client.get(url)
        ratings = Rating.objects.all()
        serializer = RatingSerializer(ratings, many=True)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], serializer.data)

    def test_list_ratings_with_filter(self):
        """
        Teste para listar avaliações com filtro por livro
        """
        url = reverse('rating-list')
        response = self.client.get(
            url,
            {'book_title': self.book.book_title, 'book_authors': self.book.book_authors}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_create_rating_authenticated(self):
        """
        Teste para criar uma avaliação (requer autenticação)
        """
        self.client.force_authenticate(user=self.user)
        url = reverse('rating-list')
        data = {
            'book_title': self.book.book_title,
            'book_authors': self.book.book_authors,
            'score': 5,
            'comment': 'Fantástico!'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Rating.objects.count(), 3)

    def test_create_rating_unauthenticated(self):
        """
        Teste para criar uma avaliação sem autenticação (deve falhar)
        """
        url = reverse('rating-list')
        data = {
            'book_title': self.book.book_title,
            'book_authors': self.book.book_authors,
            'score': 5,
            'comment': 'Fantástico!'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_rating_invalid_book(self):
        """
        Teste para criar uma avaliação com livro inexistente
        """
        self.client.force_authenticate(user=self.user)
        url = reverse('rating-list')
        data = {
            'book_title': 'Livro Inexistente',
            'book_authors': 'Autor Inexistente',
            'score': 5,
            'comment': 'Teste'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_rating_invalid_score(self):
        """
        Teste para criar uma avaliação com pontuação inválida
        """
        self.client.force_authenticate(user=self.user)
        url = reverse('rating-list')
        data = {
            'book_title': self.book.book_title,
            'book_authors': self.book.book_authors,
            'score': 6,  # Score maior que o permitido
            'comment': 'Teste'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)