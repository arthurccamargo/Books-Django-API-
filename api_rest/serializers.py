from rest_framework import serializers
from django.db.models import Avg

from .models import Book
from .models import Rating

# Serializar o modelo Book para JSON
class BookSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()
    rating_count = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = '__all__' # api vai devolver todos os campos
        
    """
    aggregate() retorna um dicionário, o nome da chave no dicionário segue o padrão <field_name>__<aggregation_function>. Assim, o campo é score e a função é Avg, 
    então a chave é score__avg
    """
    def get_average_rating(self, obj):
        return obj.ratings.aggregate(Avg('score'))['score__avg']

    def get_rating_count(self, obj):
        return obj.ratings.count()
    
class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'book', 'score', 'comment', 'created_at']