from rest_framework.routers import DefaultRouter
from .views import BookViewSet, RatingViewSet

router = DefaultRouter()
router.register(r'books', BookViewSet, basename='book')
router.register(r'ratings', RatingViewSet, basename='rating')

urlpatterns = router.urls