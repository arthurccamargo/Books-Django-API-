from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema, OpenApiExample
from rest_framework.exceptions import ValidationError
from .models import Book
from .models import Rating
from .serializers import BookSerializer
from .serializers import RatingSerializer

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


# ViewSet para o modelo Rating
@extend_schema(tags=["ratings"])
class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

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
        Lista as avaliações, permitindo filtrar pelo título e autor do livro.
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
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