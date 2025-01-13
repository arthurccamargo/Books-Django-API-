from rest_framework import serializers
from .models import Book

# Serializar o modelo Book para JSON
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__' # api vai devolver todos os campos

    