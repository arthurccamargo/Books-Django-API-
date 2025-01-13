from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema, OpenApiExample
from .models import Book
from .serializers import BookSerializer

from .services.google_books import save_books_to_db

# ViewSet para o modelo Book
@extend_schema(tags=["books"])
class BookViewSet(viewsets.ViewSet):
    """
    ViewSet para gerenciar livros.
    """
    @extend_schema(
        summary="Lista todos os livros",
        description="Retorna uma lista de todos os livros cadastrados",
        responses={200: BookSerializer(many=True)}
    )
    def list(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Cria um novo livro",
        description="Cria um novo livro com os dados fornecidos",
        request=BookSerializer,
        responses={201: BookSerializer, 400: None},
        examples=[
            OpenApiExample(
                'Valid Book',
                value={
                    'book_title': 'O Senhor dos Anéis',
                    'book_authors': 'J.R.R. Tolkien',
                    'book_description': 'Livro de Ação e Aventura',
                    'selfLink': 'www.bibliotecapublica.br/osenhordosaneis'
                }
            )
        ]
    )
    def create(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="Obtém um livro específico",
        description="Retorna os detalhes de um livro específico",
        responses={200: BookSerializer, 404: None}
    )
    def retrieve(self, request,pk=None):
        try:
            book = Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = BookSerializer(book)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Atualiza um livro",
        description="Atualiza os dados de um livro existente",
        request=BookSerializer,
        responses={200: BookSerializer, 400: None, 404: None}
    )
    def update(self, request, pk=None):
        try:
            book = Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="Remove um livro",
        description="Remove um livro do sistema",
        responses={204: None, 404: None}
    )
    def destroy(self, request,pk=None):
        try:
            book = Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @extend_schema(
        summary="Busca livros na API do Google Books e preenche o banco de dados",
        description="Busca livros com base no termo fornecido, salva os resultados no banco e retorna os livros salvos.",
        parameters=[
            {
                'name': 'q',
                'description': 'Termo de busca',
                'required': True,
                'type': 'string',
                'in': 'query'
            }
        ],
        responses={201: BookSerializer(many=True), 400: None}
    )
    @action(detail=False, methods=['get'])
    def fetch_and_save_books(self, request):
        query = request.query_params.get('q')
        if not query:
            return Response({'error': 'O parâmetro "q" é obrigatório.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Chamar o serviço para buscar e salvar os livros
            created_books = save_books_to_db(query)

            # Serializar e retornar os livros criados
            response_serializer = BookSerializer(created_books, many=True)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
