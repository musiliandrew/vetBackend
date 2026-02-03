from rest_framework import status, viewsets, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.conf import settings
from .models import User
from .serializers import UserSerializer, RegisterSerializer
import random

# Simple OTP store (replace with Redis in production)
otp_store = {}

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register_user(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            "user": UserSerializer(user).data,
            "token": token.key
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            "user": UserSerializer(user).data,
            "token": token.key
        })
    return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_profile(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def send_otp(request):
    email = request.data.get('email')
    if not email:
        return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    otp = str(random.randint(1000, 9999))
    otp_store[email] = otp
    print(f"OTP for {email}: {otp}")
    
    try:
        send_mail(
            subject='VetPathshala OTP Verification',
            message=f'Your OTP is {otp}. It is valid for 10 minutes.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )
        return Response({"message": "OTP sent successfully via email"})
    except Exception as e:
        print(f"Error sending email: {e}")
        return Response({"error": "Failed to send OTP email"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def verify_otp(request):
    email = request.data.get('email')
    otp = request.data.get('otp')
    
    if not email or not otp:
        return Response({"error": "Email and OTP are required"}, status=status.HTTP_400_BAD_REQUEST)

    if otp_store.get(email) == otp:
        # If user exists, return token, else tell front-end to register
        # We assume username or email matches
        user = User.objects.filter(email=email).first()
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                "verified": True,
                "registered": True,
                "token": token.key,
                "user": UserSerializer(user).data
            })
        return Response({"verified": True, "registered": False})
    return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)
