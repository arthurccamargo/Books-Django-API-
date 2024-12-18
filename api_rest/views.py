from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Book
from .serializers import BookSerializer

# Create your views here.
@api_view(['GET','POST'])
def book_list(request):
    # Listagem de livros
    if request.method == 'GET':
        book = Book.objects.all()
        serializer = BookSerializer(book, many= True)
        return Response(serializer.data)
    
     # Criar dados de livros
    if request.method == 'POST':
        new_book_data = request.data
        # Está serializando um dado, em vez de objeto
        serializer = BookSerializer(data=new_book_data)

        if serializer.is_valid():
            serializer.save() # Salva no banco de dados
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else: 
            return Response(status=status.HTTP_400_BAD_REQUEST)
    
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT','DELETE'])
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
        return Response(status=status.HTTP_400_BAD_REQUEST)

    # Deletar livros
    if request.method == 'DELETE':
        try:
            book.delete()
            return Response(status=status.HTTP_202_ACCEPTED)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
