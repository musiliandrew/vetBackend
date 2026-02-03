from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import SubscriptionPlan, CoinPackage, Transaction, UserSubscription
from .serializers import (
    SubscriptionPlanSerializer, CoinPackageSerializer, 
    TransactionSerializer, UserSubscriptionSerializer
)
from django.utils import timezone
from datetime import timedelta

class SubscriptionPlanViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SubscriptionPlan.objects.all()
    serializer_class = SubscriptionPlanSerializer
    permission_classes = [permissions.AllowAny]

class CoinPackageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CoinPackage.objects.all()
    serializer_class = CoinPackageSerializer
    permission_classes = [permissions.AllowAny]

class UserSubscriptionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserSubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserSubscription.objects.filter(user=self.request.user)

    @action(detail=False, methods=['post'])
    def subscribe(self, request):
        plan_id = request.data.get('plan_id')
        plan = SubscriptionPlan.objects.get(id=plan_id)
        
        # In a real app, perform payment processing here
        
        end_date = timezone.now() + timedelta(days=30 * plan.duration_months)
        sub = UserSubscription.objects.create(
            user=request.user,
            plan=plan,
            end_date=end_date
        )
        
        # Update user premium status
        request.user.is_premium = True
        request.user.save()
        
        return Response(UserSubscriptionSerializer(sub).data)

class CoinPurchaseViewSet(viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['post'])
    def purchase(self, request):
        package_id = request.data.get('package_id')
        package = CoinPackage.objects.get(id=package_id)
        
        # In a real app, perform payment processing here
        
        Transaction.objects.create(
            user=request.user,
            amount=package.price,
            transaction_type='COIN',
            status='SUCCESS'
        )
        
        # Update user balance
        request.user.coin_balance += package.coins_amount
        request.user.save()
        
        return Response({"new_balance": request.user.coin_balance})
