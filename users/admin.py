from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'phone_number', 'role', 'coin_balance', 'is_premium')
    search_fields = ('username', 'phone_number')
