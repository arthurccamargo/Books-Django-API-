from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema, OpenApiExample
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Book, Rating
from .serializers import BookSerializer, RatingSerializer
from .services.google_books import save_books_to_db
from django.shortcuts import render
from .export_utils import export_books_csv, export_ratings_csv

# ViewSet para o modelo Book
@extend_schema(tags=["books"])
class BookViewSet(viewsets.ViewSet):
    # Sobreescrevendo método get_permissions de ViewSet
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated()]
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
        paginator = PageNumberPagination()
        # Divide o conjunto de dados de acordo com o número de itens por página definido na classe BookPagination
        paginated_books = paginator.paginate_queryset(books, request)
        # Os registros da página solicitada são serializados
        serializer = BookSerializer(paginated_books, many=True)
        return paginator.get_paginated_response(serializer.data)

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

    # http://127.0.0.1:8000/api/books/fetch_and_save_books/?q=aventura - exemplo de uso
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


# ViewSet para o modelo Rating
@extend_schema(tags=["ratings"])
class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

    # Sobreescrevendo método get_permissions no ViewSet
    def get_permissions(self):
        if self.action in ['list', 'get_queryset', 'retrieve']:
            return [AllowAny()] # Permite acesso público para listar ou visualizar avaliações
        return [IsAuthenticated()] # Requer autenticação para as demais ações

    @extend_schema(
        summary="Cria uma nova avaliação",
        description="Cria uma avaliação associada a um livro com base no título e autor fornecidos.",
        request=RatingSerializer,
        responses={201: RatingSerializer, 400: None},
        examples=[
            OpenApiExample(
                'Valid Rating',
                value={
                    'book_title': 'O Senhor dos Anéis',
                    'book_authors': 'Gerald',
                    'score': 5,
                    'comment': 'Um livro épico e envolvente!'
                }
            )
        ]
    )
    def create(self, request, *args, **kwargs):
        """
        Cria uma avaliação com base no título e autor do livro.
        """
        book_title = request.data.get('book_title')
        book_authors = request.data.get('book_authors')

        if not book_title or not book_authors:
            raise ValidationError({"error": "Os campos 'book_title' e 'book_authors' são obrigatórios."})

        try:
            book = Book.objects.get(book_title=book_title, book_authors=book_authors)
        except Book.DoesNotExist:
            raise ValidationError({"error": "O livro com o título e autor informados não existe."})

        data = request.data.copy()
        data['book'] = book.id

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        """
        Filtra as avaliações com base no título e autor do livro fornecidos nos query_params.
        Exemlo de uso na URL: http://127.0.0.1:8000/api/ratings/?book_title=O Senhor dos Anéis&book_authors=Gerald
        """
        queryset = super().get_queryset()

        # Obtém os parâmetros da URL (query_params)
        book_title = self.request.query_params.get('book_title')
        book_authors = self.request.query_params.get('book_authors')

        # Verifica se os parâmetros obrigatórios estão presentes
        if book_title and book_authors:
            try:
                # Busca o livro pelo título e autor
                book = Book.objects.get(book_title=book_title, book_authors=book_authors)
                # Filtra as avaliações relacionadas ao livro encontrado
                queryset = queryset.filter(book=book.id)
            except Book.DoesNotExist:
                # Lança um erro se o livro não for encontrado
                raise ValidationError({"error": "Nenhum livro encontrado com o título e autor fornecidos."})

        return queryset
    
    @extend_schema(
        summary="Lista avaliações",
        description=(
            "Retorna uma lista de avaliações. Você pode filtrar as avaliações pelo título e autor do livro "
            "usando os parâmetros 'book_title' e 'book_authors'."
        ),
        parameters=[
            {
                'name': 'book_title',
                'description': 'Título do livro para filtrar as avaliações.',
                'required': False,
                'type': 'string',
                'in': 'query',
            },
            {
                'name': 'book_authors',
                'description': 'Autor do livro para filtrar as avaliações.',
                'required': False,
                'type': 'string',
                'in': 'query',
            },
        ],
        responses={200: RatingSerializer(many=True), 400: None}
    )
    def list(self, request, *args, **kwargs):
        """
        Lista as avaliações com paginação, permitindo filtrar pelo título e autor do livro.
        """
        queryset = self.get_queryset()
        # Paginador padrão do DRF
        page = self.paginate_queryset(queryset) # dividi o queryset em páginas
        if page is not None:
            serializer = RatingSerializer(page, many=True) # serializa apenas os itens daquela página
            return self.get_paginated_response(serializer.data) # resposta paginada

        # Caso não exista paginação, retorne todos os itens
        serializer = RatingSerializer(queryset, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Exclui uma avaliação",
        description="Remove uma avaliação específica com base no ID.",
        responses={204: None, 404: None}
    )
    def destroy(self, request, *args, **kwargs):
        """
        Sobrescreve o método destroy para garantir uma resposta consistente.
        """
        return super().destroy(request, *args, **kwargs)
    
def export_books_view(request):
    return export_books_csv()

def export_ratings_view(request):
    return export_ratings_csv()