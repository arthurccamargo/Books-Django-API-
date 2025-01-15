from rest_framework.routers import DefaultRouter
from .views import BookViewSet, RatingViewSet, export_books_view, export_ratings_view
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

router = DefaultRouter()
router.register(r'books', BookViewSet, basename='book')
router.register(r'ratings', RatingViewSet, basename='rating')

urlpatterns = [
    # Rotas padrão do JWT
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    # Exportação de dados CSV
    path('export/books/', export_books_view, name='export_books_view'),
    path('export/ratings/', export_ratings_view, name='export_ratings_view'),
]

urlpatterns += router.urls