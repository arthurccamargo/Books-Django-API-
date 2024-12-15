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


@api_view(['GET', 'PUT', 'DELETE'])
def get_by_id(request, id):
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

    if request.method == 'DELETE':
        try:
            book.delete()
            return Response(status=status.HTTP_202_ACCEPTED)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    
@api_view(['GET','POST','PUT'])
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
        

 # Editar dados de livros
    if request.method == 'PUT':
        
        # Captura o valor da chave titulo do livro que quero editar do corpo do request 
        title = request.data.get("book_title")

        if not title:
            return Response({"error": "O campo 'book_title' é obrigatório."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                # Captura objeto livro que possui esse titulo no banco de dados
                update_book = Book.objects.get(book_title=title)
            except:
                return Response(status=status.HTTP_404_NOT_FOUND)
            
            # Objeto update_book sera editado e coloca os novos dados de request.data 
            serializer = BookSerializer(update_book, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
            else:
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
