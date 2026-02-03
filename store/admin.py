from django.contrib import admin
from .models import SubscriptionPlan, CoinPackage, Transaction, UserSubscription

admin.site.register(SubscriptionPlan)
admin.site.register(CoinPackage)
admin.site.register(Transaction)
admin.site.register(UserSubscription)
