from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SubscriptionPlanViewSet, CoinPackageViewSet, UserSubscriptionViewSet, CoinPurchaseViewSet

router = DefaultRouter()
router.register(r'plans', SubscriptionPlanViewSet)
router.register(r'packages', CoinPackageViewSet)
router.register(r'my-subscriptions', UserSubscriptionViewSet, basename='my-subscriptions')

urlpatterns = [
    path('', include(router.urls)),
    path('buy-coins/', CoinPurchaseViewSet.as_view({'post': 'purchase'}), name='buy_coins'),
]
