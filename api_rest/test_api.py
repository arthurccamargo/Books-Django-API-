from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Book, Rating

class APITests(TestCase):
    def setUp(self):
        # Criando um usuário de teste
        self.user = get_user_model().objects.create_user(username='arthur', password='senhasenha')
        self.client = APIClient()  # Criando o cliente para fazer as requisições

    def get_token(self):
        """Função para obter o token JWT"""
        # Obtém o token de acesso
        response = self.client.post('/token/', {'username': 'arthur', 'password': 'senhasenha'})
        return response.data['access']  # Retorna o token de acesso
    
    