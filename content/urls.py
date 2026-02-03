from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BannerViewSet, TestimonialViewSet, DrugViewSet, BookViewSet, BookCategoryViewSet

router = DefaultRouter()
router.register(r'banners', BannerViewSet)
router.register(r'testimonials', TestimonialViewSet)
router.register(r'drugs', DrugViewSet)
router.register(r'books', BookViewSet)
router.register(r'ebook-categories', BookCategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
