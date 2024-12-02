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