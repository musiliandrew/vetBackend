from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Role(models.TextChoices):
        STUDENT = 'STUDENT', 'Student'
        DOCTOR = 'DOCTOR', 'Doctor'
        ADMIN = 'ADMIN', 'Admin'

    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.STUDENT)
    language_preference = models.CharField(max_length=5, default='en')
    
    # Wallet/Profile fields can be connected via OneToOne or directly here if simple
    coin_balance = models.IntegerField(default=0)
    is_premium = models.BooleanField(default=False)

    def __str__(self):
        return self.username
