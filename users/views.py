from rest_framework import status, viewsets, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
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
    phone = request.data.get('phone')
    if not phone:
        return Response({"error": "Phone number is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    otp = str(random.randint(1000, 9999))
    otp_store[phone] = otp
    print(f"OTP for {phone}: {otp}")
    
    return Response({"message": "OTP sent successfully", "otp": otp})

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def verify_otp(request):
    phone = request.data.get('phone')
    otp = request.data.get('otp')
    if otp_store.get(phone) == otp:
        # If user exists, return token, else tell front-end to register
        user = User.objects.filter(phone_number=phone).first()
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
