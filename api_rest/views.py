from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Book
from .serializers import BookSerializer

import json

# Create your views here.
@api_view(['GET'])
def get_books(request):
    if request.method == 'GET':
        book = Book.objects.all()
        serializer = BookSerializer(book, many= True)
        return Response(serializer.data)
    
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_by_id(request, id):
    try:
        book = Book.objects.get(pk=id)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = BookSerializer(book)
        return Response(serializer.data)
    
@api_view(['GET'])
def book_manager(request):
    if request.method == 'GET':
        # Verifica se o parametro title foi enviado
        book_title = request.GET.get('title', None)

        if not book_title:
            return Response(
                    {"error": "O parametro title é obrigatório"},
                    status=status.HTTP_400_BAD_REQUEST
            )
    
        try:
            # Buscar o livro pelo titulo
            book = Book.objects.get(book_title=book_title) 
        except Book.DoesNotExist:
            return Response(
                {"error": "Livro não encontrado."},
                status=status.HTTP_404_NOT_FOUND # Nao encontrou o objeto
                ) 
        except Exception as e:
            return Response(
                {"error": f"Ocorreu um erro: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # Serializar e retorna os dados do livro
        serializer = BookSerializer(book)
        return Response(serializer.data)