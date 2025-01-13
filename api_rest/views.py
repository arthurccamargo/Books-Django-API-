from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Book
from .serializers import BookSerializer
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample

@extend_schema(
    tags=['books'],
    methods=['GET'],
    summary="Lista todos os livros",
    description="Retorna uma lista de todos os livros cadastrados",
    responses={200: BookSerializer(many=True)}
)
@extend_schema(
    methods=['POST'],
    summary="Cria um novo livro",
    description="Cria um novo livro com os dados fornecidos",
    request=BookSerializer,
    responses={
        201: BookSerializer,
        400: None
    },
    examples=[
        OpenApiExample(
            'Valid Book',
            value={
                'book_title': 'O Senhor dos Anéis',
                'book_authors': 'J.R.R. Tolkien',
                'book_description':'Livro de Ação e Aventura',
                'selfLink': 'www.bibliotecapublica.br/osenhordosaneis'
            }
        )
    ]
)
@api_view(['GET', 'POST'])
def book_list(request):
    if request.method == 'GET':
        book = Book.objects.all()
        serializer = BookSerializer(book, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # Criar dados de livros
    if request.method == 'POST':
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    tags=['books'],
    methods=['GET'],
    summary="Obtém um livro específico",
    description="Retorna os detalhes de um livro específico",
    responses={
        200: BookSerializer,
        404: None
    }
)
@extend_schema(
    methods=['PUT'],
    summary="Atualiza um livro",
    description="Atualiza os dados de um livro existente",
    request=BookSerializer,
    responses={
        200: BookSerializer,
        400: None,
        404: None
    }
)
@extend_schema(
    methods=['DELETE'],
    summary="Remove um livro",
    description="Remove um livro do sistema",
    responses={
        204: None,
        404: None
    }
)
@api_view(['GET', 'PUT', 'DELETE'])
def book_manager(request, id):
    try:
        book = Book.objects.get(pk=id)
    except Book.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = BookSerializer(book)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    if request.method == 'PUT':
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # Deletar livros
    if request.method == 'DELETE':
        try:
            book.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
